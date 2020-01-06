import sqlite3
import pandas as pd
import json


def to_df(db_path):
    header = []
    conn = sqlite3.connect(path)
    c = conn.cursor()
    for column in c.execute('PRAGMA table_info("Choice")'):
        header.append(column[1])

    df = pd.DataFrame(columns=header)
    for raw in c.execute('SELECT * FROM Choice ORDER BY id'):
        s = pd.Series(list(raw), index=df.columns)
        df = df.append(s, ignore_index=True)
    return df


if __name__ == '__main__':
    path = '../../flaski/test.db'
    df = to_df(path)
    df.to_csv('../data/choice.csv')
    f = open('../data/choice.json', 'w')
    json_data = json.loads(df.to_json(orient='records'))
    json.dump(json_data, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))
