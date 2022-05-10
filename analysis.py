# Script for extracting word order distributions from CONLLU files

import sys
import random
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

pd.set_option('display.max_rows', None)

print_dist    = '-d' in sys.argv
print_ex      = '-e' in sys.argv
plot_heatmap  = '-h' in sys.argv
make_datafile = '-f' in sys.argv
make_cov_mat  = '-c' in sys.argv

use_aux       = '-x' in sys.argv
use_iobj      = '-i' in sys.argv
only_sov_p    = '-p' in sys.argv

sov_perms = ['SOV', 'OSV', 'VSO', 'VOS', 'SVO', 'OVS']

def main():
    if len(sys.argv) < 3:
        print('Add an argument for the corpus collection file, and a path prefix.')
        return
    if only_sov_p and (use_aux or use_iobj):
        print('-p is incompatible with -x and -i.')
        return
    if plot_heatmap and not only_sov_p:
        print('Heatmap is not yet implemented for full distributions.')
        return
    langs = []
    results = []
    with open(sys.argv[1]) as lang_paths:
        for lang_path in lang_paths:
            lang, path = lang_path.split()
            langs.append(lang)
            results.append(analyse_corpus(lang, sys.argv[2] + path))
    if plot_heatmap or make_cov_mat:
        table = []
        for freq in results:
            table.append([(freq[o] if o in freq else 0) for o in sov_perms])
        if plot_heatmap:
            data = pd.DataFrame(table, columns = sov_perms, index = langs)
            sns.clustermap(data, yticklabels = True, col_cluster = False)
            plt.show()
        if make_cov_mat:
            print(np.cov(np.transpose(table)))
    if make_datafile:
        file = open('distributions.txt', 'w')
        for lang, result in zip(langs, results):
            file.write(lang + ' ' + str(result) + '\n')
        file.close()

def analyse_corpus(language, path):
    print('Analysing', language, end = '. ')
    sys.stdout.flush()
    order_count = {}
    examples = {}
    with open(path) as f:
        sentence = []
        for line in f:
            if line.strip() != '':
                sentence.append(line.strip())
            else:
                data, text = parse(sentence)
                sentence = []
                result = orders_in_sentence(data)
                for o, ex in result:
                    if only_sov_p and not o in sov_perms:
                        continue
                    if o not in order_count:
                        order_count[o] = 0
                        examples[o] = []
                    order_count[o] += 1
                    if print_ex:
                        examples[o].append(ex)
    total = sum(order_count.values())
    print('Found', total, 'clauses.')
    orders_desc = sorted(order_count.keys(), key = lambda o: order_count[o], reverse = True)
    if print_dist or print_ex:
        for o in orders_desc:
            print(o + ': ' + str(order_count[o]))
            if print_ex:
                exs = random.sample(examples[o], min(5, len(examples[o])))
                for i in range(len(exs)):
                    print(str(i + 1) + '.', exs[i])
    return {order: count / total for order, count in order_count.items()}

def parse(sentence):
    text = list(filter(lambda t: t[0] == '#' and 'text' in t, sentence))
    tokens = list(filter(lambda t: t[0] != '#', sentence))
    data = {}
    for t in tokens:
        try:
            id, form, lemma, upos, xpos, feats, head, deprel, deps, misc = t.split('\t')
            if '.' in id or '-' in id:
                continue
            id = int(id)
            head = int(head)
        except BaseException as e:
            print('Error at', t)
            print(e)
        deprel = deprel.split(':')[0]
        data[id] = {'form': form, 'lemma': lemma, 'upos': upos, 'xpos': xpos, 'feats': feats, 'head': head, 'deprel': deprel, 'deps': deps, 'misc': misc}
    return data, text

def orders_in_sentence(data):
    n = 0
    verb_ids = []
    for id in data.keys():
        if data[id]['upos'] == 'VERB':
            verb_ids.append(id)
    result = []
    for v_id in verb_ids:
        l = [(v_id, 'V')]
        for id in data.keys():
            if data[id]['head'] == v_id:
                if data[id]['deprel'] == 'nsubj':
                    l.append((id, 'S'))
                if data[id]['deprel'] == 'obj':
                    l.append((id, 'O'))
                if use_iobj and data[id]['deprel'] == 'iobj':
                    l.append((id, 'I'))
                if use_aux and data[id]['deprel'] == 'aux':
                    l.append((id, 'X'))
        order = ''.join([letter for (id, letter) in sorted(l)])
        before = sorted(filter(lambda id: id < v_id, data.keys()))
        after = sorted(filter(lambda id: id > v_id, data.keys()))
        text = ' '.join(data[id]['form'] for id in before) + ' [' + data[v_id]['form'] + '] ' + ' '.join(data[id]['form'] for id in after)
        result.append((order, text))
    return result

if __name__ == '__main__':
    main()