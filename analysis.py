# Script for extracting word order distributions from CONLLU files
import os 
from tabulate import tabulate
import sys

def main():
    #bygger om word-orders.txt varje gång programmet körs. 
    #kanske onödigt, men då kommer åtmistone correlation.py alltid hänga med på förändringar
    if os.path.exists("word-orders.txt"):
        os.remove("word-orders.txt")
    wo = open ("word-orders.txt", "w" )
    if len(sys.argv) == 1:
        print('Add an argument for the corpus collection file')
        return
    table = []
    with open(sys.argv[1]) as lang_paths:
        for lang_path in lang_paths:
            language, path = lang_path.split()
            #Nu är return-värdet för analyse_corpus aningen lägre. så det krävs lite meck med det
            analysis = analyse_corpus(language, path) 
            table.append([language] + analysis[:2])
            wo.write(str(language) + ': ' + str(analysis[-1]) +'\n')

    table.sort(key = lambda x: x[2], reverse = True)
    print(tabulate(table,
        headers = ['Language', 'Sentences', 'SV/S', 'OV/O'],
        floatfmt = '.4f'
    ))
    wo.close()
def analyse_corpus(language, path):
    print('Analysing', language) 
     
    word_orders = {}
    with open(path, encoding='utf8') as f:
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
        proportion(lambda x: 'O' in x[1].split('V')[0], lambda x: 'O' in x[1]),
        word_orders #vill ha med word_orders, det är vad jag vill ha in word-orders.txt
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
                # if data[id]['deprel'] == 'iobj': ## jag vill ignorera dessa
                #     l.append((id, 'I'))
                # if data[id]['deprel'] == 'aux':
                #     l.append((id, 'X'))
        orders.append(''.join([letter for (id, letter) in sorted(l)]))
    return orders

if __name__ == '__main__':
    main()