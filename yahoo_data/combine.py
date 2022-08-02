#Combine raw data from yahoo as source data for fx service
#1. Note that fx closing time zone is not the same
#2. Will just use the close price since this is the only data I have
#3. Not worried about holidays, all data source have same number of days

import pandas as pd
import sqlite3

table_name = 'fx'

def combine(curs: list[str]):
    dfs = []
    columns = ['Date','Currency','Close']

    for cur in curs:
        tmp_df = pd.read_csv(cur + "=x.csv")
        tmp_df['Currency'] = cur
        dfs.append(tmp_df)

    df_main = pd.concat(dfs,ignore_index=True)
    df_main = df_main[columns]
    df_main['Date'] = pd.to_datetime(df_main['Date'], format='%Y-%m-%d').dt.strftime('%Y-%m-%d %H:%M:%S')
    df_main.to_csv(table_name + '.csv',index=False)

def convertToDB():
    df_main = pd.read_csv(table_name + '.csv')

    conn = sqlite3.connect(table_name + '.db')
    create_sql = 'CREATE TABLE IF NOT EXISTS ' + table_name + ' ('
    create_sql += 'Date TEXT NOT NULL,'
    create_sql += 'Currency TEXT NOT NULL,'
    create_sql += 'Close REAL NOT NULL,'
    create_sql += 'PRIMARY KEY (Date, Currency)'
    create_sql += ');'

    print(create_sql)
    cursor = conn.cursor()
    cursor.execute(create_sql)

    for irow in df_main.itertuples():
        insert_values_string = ''.join(['INSERT INTO ', table_name, ' VALUES ('])
        insert_sql = f"{insert_values_string} '{irow[1]}', '{irow[2]}',{irow[3]} )"
        print(insert_sql)
        cursor.execute(insert_sql)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    curs = ['AUD','CAD','JPY']
    combine(curs)
    convertToDB()