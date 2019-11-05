import json
from statistics import mean, stdev
from scipy.stats import f_oneway

def read():
	data = json.load(open('flaski/choice.json'))
	return data

def output(data):
    names = ['Chaturvedi', 'FDGIB', 'STGIB', 'TRGIB']
    list = [ [{ "answer": [], "time":[]} for i in range(4)] for j in range(4)]
    for datum in data:
        if datum['layout'] == 'Chatu':
            list[int(datum['task'])-1][0]['answer'].append(int(datum['answer']))
            list[int(datum['task'])-1][0]['time'].append(float(datum['time'])) 
        elif datum['layout'] == 'FDGIB':
            list[int(datum['task'])-1][1]['answer'].append(int(datum['answer']))
            list[int(datum['task'])-1][1]['time'].append(float(datum['time']))
        elif datum['layout'] == 'STGIB':
            list[int(datum['task'])-1][2]['answer'].append(int(datum['answer']))
            list[int(datum['task'])-1][2]['time'].append(float(datum['time']))
        elif datum['layout'] == 'TRGIB':
            list[int(datum['task'])-1][3]['answer'].append(int(datum['answer']))
            list[int(datum['task'])-1][3]['time'].append(float(datum['time']))
    outputs= [ [{} for i in range(4)] for j in range(4)]
    for task in range(4):
        for layout in range(4):
            try:
                ans = mean(list[task][layout]['answer'])
                dev_ans = stdev(list[task][layout]['answer'])
                time = mean(list[task][layout]['time'])
                dev_time = stdev(list[task][layout]['time'])
                outputs[task][layout]['ans'] = ans
                outputs[task][layout]['dev_ans'] = dev_ans
                outputs[task][layout]['time'] = time
                outputs[task][layout]['dev_time'] = dev_time
                outputs[task][layout]['layout'] = names[layout]
            except:
                pass

    f = open('./flaski/statistics.json', 'w')
    json.dump(outputs, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))


def main():
    data = read()
    output(data)
    answers = [[[] for j in range(4)] for i in range(4)]
    times = [[[] for j in range(4)] for i in range(4)]
    for datum in data:
        if datum['layout'] == 'Chatu':
            layout = 1
        elif datum['layout'] == 'FDGIB':
            layout = 2
        elif datum['layout'] == 'STGIB':
            layout = 0
        elif datum['layout'] == 'TRGIB':
            layout = 3
        answers[int(datum['task']) - 1][layout].append(int(datum['answer']))
        times[int(datum['task']) - 1][layout].append(int(datum['time']))

    result1 = f_oneway(answers[0][0], answers[0][1], answers[0][2], answers[0][3])
    result2 = f_oneway(answers[1][0], answers[1][1], answers[1][2], answers[1][3])
    result3 = f_oneway(answers[2][0], answers[2][1], answers[2][2], answers[2][3])
    result4 = f_oneway(answers[3][0], answers[3][1], answers[3][2], answers[3][3])
    print(result1.pvalue, result2.pvalue, result3.pvalue, result4.pvalue)

    result1 = f_oneway(times[0][0], times[0][1], times[0][2], times[0][3])
    result2 = f_oneway(times[1][0], times[1][1], times[1][2], times[1][3])
    result3 = f_oneway(times[2][0], times[2][1], times[2][2], times[2][3])
    result4 = f_oneway(times[3][0], times[3][1], times[3][2], times[3][3])
    print(result1.pvalue, result2.pvalue, result3.pvalue, result4.pvalue)

if __name__ == '__main__':
    main()
