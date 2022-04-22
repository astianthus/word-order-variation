import sys

def parse(sentence):
    tokens = list(filter(lambda t: t[0] != '#', sentence))
    data = {}
    for t in tokens:
        try:
            id, form, lemma, upos, xpos, feats, head, deprel, deps, misc = t.split('\t')
            if '.' in id:
                continue
            id = int(id)
            head = int(head)
        except BaseException as e:
            print('Error at', t)
            print(e)
        data[id] = {'form': form, 'lemma': lemma, 'upos': upos, 'xpos': xpos, 'feats': feats, 'head': head, 'deprel': deprel, 'deps': deps, 'misc': misc}
    return data

def analyse(data):
    n = 0
    verb_ids = []
    for id in data.keys():
        if data[id]['upos'] == 'VERB':
            verb_ids.append(id)
    orders = []
    for v_id in verb_ids:
        nsubj = 0
        obj = 0
        for id in data.keys():
            if data[id]['head'] == v_id:
                if data[id]['deprel'] == 'nsubj':
                    if nsubj != 0:
                        print('WARNING: Many subjects found')
                    nsubj = id
                if data[id]['deprel'] == 'obj':
                    if obj != 0:
                        print('WARNING: Many objects found')
                    obj = id
        l = [(v_id, 'V')]
        if nsubj != 0:
            l.append((nsubj, 'S'))
        if obj != 0:
            l.append((obj, 'O'))
        orders.append(''.join([letter for (id, letter) in sorted(l)]))
    return orders

def main():
    if len(sys.argv) != 2:
        print('Add an argument for the corpus file')
        return
    word_orders = {}
    with open(sys.argv[1]) as f:
        sentence = []
        for line in f:
            if line.strip() != '':
                sentence.append(line.strip())
            else:
                data = parse(sentence)
                sentence = []
                result = analyse(data)
                for o in result:
                    if o not in word_orders:
                        word_orders[o] = 0
                    word_orders[o] += 1
    word_orders = [(word_orders[o], o) for o in word_orders]
    word_orders.sort(reverse = True)
    print(word_orders)

if __name__ == '__main__':
    main()