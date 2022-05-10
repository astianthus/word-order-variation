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