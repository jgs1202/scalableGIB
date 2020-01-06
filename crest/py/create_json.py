import json
import sys
import pandas as pd


def read_data():
    node_path = '../data/QPC421.txt'
    link_path = '../data/20181105-CORR-33WT.txt'
    node_data = pd.read_table(node_path)
    link_data = pd.read_table(link_path)
    print(link_data)


if __name__ == '__main__':
    read_data()