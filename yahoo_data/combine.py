#Combine raw data from yahoo as source data for fx service
#1. Note that fx closing time zone is not the same
#2. Will just use the close price since this is the only data I have
#3. Not worried about holidays, all data source have same number of days

import pandas as pd

def combine(curs):
    dfs = []
    columns = ['Date','Currency','Close']

    for cur in curs:
        tmp_df = pd.read_csv(cur+"=x.csv")
        tmp_df['Currency'] = cur
        dfs.append(tmp_df)

    df_main = pd.concat(dfs,ignore_index=True)
    df_main = df_main[columns]
    df_output = df_main.pivot(index='Date',columns='Currency',values='Close')
    df_output.to_csv('fx.csv')


if __name__ == "__main__":
    curs = ['AUD','CAD','JPY']
    combine(curs)