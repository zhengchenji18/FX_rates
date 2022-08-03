"""
Combine raw data from yahoo as source data for fx service
1. Note that fx closing time zone is not the same
2. Will just use the close price since this is the only data I have
3. Not worried about holidays, all data source have same number of days
   potentially need to build a holidays class in the future
"""

import sqlite3
import pandas as pd

TABLE_NAME = 'fx'


def combine(curs: list[str]):
    """ combine raw yahoo currency data"""
    dfs = []
    columns = ['Date','Currency','Close']

    for cur in curs:
        tmp_df = pd.read_csv(cur + "=x.csv")
        tmp_df['Currency'] = cur
        dfs.append(tmp_df)

    df_main = pd.concat(dfs,ignore_index=True)
    df_main = df_main[columns]
    df_main['Date'] = pd.to_datetime(df_main['Date'], format='%Y-%m-%d'). \
                        dt.strftime('%Y-%m-%d %H:%M:%S')
    df_main.to_csv(TABLE_NAME + '.csv',index=False)


def convert_to_db():
    """create fx table from the combined yahoo data table"""
    df_main = pd.read_csv(TABLE_NAME + '.csv')

    conn = sqlite3.connect(TABLE_NAME + '.db')
    create_sql = 'CREATE TABLE IF NOT EXISTS ' + TABLE_NAME + ' ('
    create_sql += 'Date TEXT NOT NULL,'
    create_sql += 'Currency TEXT NOT NULL,'
    create_sql += 'Close REAL NOT NULL,'
    create_sql += 'PRIMARY KEY (Date, Currency)'
    create_sql += ');'

    print(create_sql)
    cursor = conn.cursor()
    cursor.execute(create_sql)

    for irow in df_main.itertuples():
        insert_values_string = ''.join(['INSERT INTO ', TABLE_NAME, ' VALUES ('])
        insert_sql = f"{insert_values_string} '{irow[1]}', '{irow[2]}',{irow[3]} )"
        print(insert_sql)
        cursor.execute(insert_sql)

    conn.commit()
    conn.close()

def main():
    """main function initate process"""
    curs = ['AUD','CAD','JPY']
    combine(curs)
    convert_to_db()

if __name__ == "__main__":
    main()
