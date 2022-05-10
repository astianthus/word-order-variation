<<<<<<< HEAD
# takes distributions.txt and searches through it for two word orders given with a command line argument
# serches for these word orders across all the languages in distributions.txt and prints out how much they correlate.
# throws a bunch of warnings at you if the at least one of the command line arguments can not be found anywhere
# Does not have a return value, so good luck imorting it anywhere

import ast
import sys
import numpy as np           

def main (command_line):
    # the frst word order and second word order 
    first = (str(command_line[1])).upper()      
    second = (str(command_line[2])).upper() 
    # list of all the values of the first word order and second word order
    x = []                          
    y = []    

    with open("distributions.txt", 'r', encoding = "utf8") as f:  
        lines = f.readlines()
        for line in lines:
            language = line.split()[0]
            orders = (line[line.find('{'):])
            orders = ast.literal_eval(orders)
            keys = list(orders.keys())
            
            if first in keys and second in keys:
                x.append(orders[first]) 
                y.append(orders[second])

        
    correlation = (np.corrcoef(x,y))[0,1]
    print (first, "correlates with", second, "with a Pearsons coeficient of: \n", correlation)
   

if __name__ == '__main__':
    main(sys.argv)
=======
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
>>>>>>> 2b5d7d064099e44f66cadae7af70ff2421eff592