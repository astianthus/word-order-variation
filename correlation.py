import ast
import sys
import random
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def read_dists():
    result = []
    with open('distributions.txt') as lang_dists:
        for lang_dist in lang_dists:
            lang, dist_str = lang_dist.split('{')
            dist = ast.literal_eval('{' + dist_str)
            result.append((lang, dist))
    return result

def main():
    o1, o2 = sys.argv[1:]
    data = read_dists()
    x, y = [], []
    for lang, dist in data:
        x.append(dist[o1] if o1 in dist else 0)
        y.append(dist[o2] if o2 in dist else 0)
    plt.scatter(x, y)
    plt.show()

if __name__ == '__main__':
    main()
