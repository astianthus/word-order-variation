# Takes output from analysis.py and, for each language, calculates a correlation for each word order and every other word order.
# It presents the correlations numerically, and writes them to a file.
import ast
def correlate(orders):
    for keys in orders.keys():
        
def main ():
    with open("distributions.txt", 'r', encoding = "utf8") as f:
        lines = f.readlines()
        for line in lines:
            language = line.split()[0]
            orders = (line[line.find('{'):])
            orders = ast.literal_eval(orders)
            correlate(orders)           


if __name__ == '__main__':
    main()