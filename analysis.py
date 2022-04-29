# Script for extracting word order distributions from CONLLU files

from tabulate import tabulate
import sys

def main():
    if len(sys.argv) == 1:
        print('Add an argument for the corpus collection file')
        return
    table = []
    with open(sys.argv[1]) as lang_paths:
        for lang_path in lang_paths:
            language, path = lang_path.split()
            table.append([language] + analyse_corpus(language, path))
    table.sort(key = lambda x: x[2], reverse = True)
    print(tabulate(table,
        headers = ['Language', 'Sentences', 'SV/S', 'OV/O'],
        floatfmt = '.4f'
    ))

def analyse_corpus(language, path):
    print('Analysing', language)
    word_orders = {}
    with open(path) as f:
        sentence = []
        for line in f:
            if line.strip() != '':
                sentence.append(line.strip())
            else:
                data, text = parse(sentence)
                sentence = []
                result = orders_in_sentence(data)
                for o in result:
                    if o not in word_orders:
                        word_orders[o] = 0
                    word_orders[o] += 1
    word_orders = [(word_orders[o], o) for o in word_orders]
    word_orders.sort(reverse = True)

    def proportion(l_feature, l_sample):
        feature = sum(n for (n, o) in filter(l_feature, word_orders))
        sample = sum(n for (n, o) in filter(l_sample, word_orders))
        return feature / sample

    return [
        sum(n for (n, o) in word_orders),
        proportion(lambda x: 'S' in x[1].split('V')[0], lambda x: 'S' in x[1]),
        proportion(lambda x: 'O' in x[1].split('V')[0], lambda x: 'O' in x[1])
    ]

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
        data[id] = {'form': form, 'lemma': lemma, 'upos': upos, 'xpos': xpos, 'feats': feats, 'head': head, 'deprel': deprel, 'deps': deps, 'misc': misc}
    return data, text

def orders_in_sentence(data):
    n = 0
    verb_ids = []
    for id in data.keys():
        if data[id]['upos'] == 'VERB':
            verb_ids.append(id)
    orders = []
    for v_id in verb_ids:
        l = [(v_id, 'V')]
        for id in data.keys():
            if data[id]['head'] == v_id:
                if data[id]['deprel'] == 'nsubj':
                    l.append((id, 'S'))
                if data[id]['deprel'] == 'obj':
                    l.append((id, 'O'))
                if data[id]['deprel'] == 'iobj':
                    l.append((id, 'I'))
                if data[id]['deprel'] == 'aux':
                    l.append((id, 'X'))
        orders.append(''.join([letter for (id, letter) in sorted(l)]))
    return orders

if __name__ == '__main__':
    main()