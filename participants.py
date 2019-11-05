import json
from statistics import mean, stdev
from scipy.stats import f_oneway


def read():
    data = json.load(open('flaski/choice.json'))
    return data


def output(data):
    names = []
    males = []
    females = []
    age = []

    for datum in data:
        name = datum['username']
        if name not in names:
            names.append(name)
        if datum['gender'] == 'Male':
            males.append(name)
        else:
            females.append(name)
        age.append(int(datum['age']))
    print(mean(age))
    print(max(age), min(age))
    print(len(males), len(females))

def main():
    data = read()
    output(data)
if __name__ == '__main__':
    main()
