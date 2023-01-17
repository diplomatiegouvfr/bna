import pandas as pd
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


def file_count_data(data_path):
    file=open(data_path, 'r', encoding="utf-8")
    data = file.readlines()
    ordered_datas = {
        'très satisfaisant' : len([sent for sent in data if all(elem in sent for elem in [' satisfaisant.', ' tres '])]),
        'satisfaisant' : len([sent for sent in data if (' satisfaisant.' in sent) and not any(elem in sent for elem in [' assez ', ' tres '])]),
        'assez satisfaisant' : len([sent for sent in data if all(elem in sent for elem in [' satisfaisant.', ' assez '])]),
        'très passable' : len([sent for sent in data if all(elem in sent for elem in [' passable.', ' tres '])]),
        'passable' : len([sent for sent in data if (' passable.' in sent) and not any(elem in sent for elem in [' assez ', ' tres '])]),
        'assez passable' : len([sent for sent in data if all(elem in sent for elem in [' passable.', ' assez '])]),
        'assez insatisfaisant' : len([sent for sent in data if all(elem in sent for elem in [' insatisfaisant.', ' assez '])]),
        'insatisfaisant' : len([sent for sent in data if (' insatisfaisant.' in sent) and not any(elem in sent for elem in [' assez ', ' tres '])]),
        'très insatisfaisant' : len([sent for sent in data if all(elem in sent for elem in [' insatisfaisant.', ' tres '])]),
        }
    # ordered_values = list(ordered_datas.values())
    # ordered_files = list(ordered_datas.keys())
    return ordered_datas


def timestamp_data(path, COL_NAME, COL_NAME_H):
    df = pd.read_excel(path, engine='openpyxl')
    df = df[df[COL_NAME].notna()]
    
    df_date = df[[COL_NAME]]
    
    df_date['Eff'] = 1
    df_autocomplete = pd.DataFrame() # initializing a new dataframe
    df_autocomplete[COL_NAME] = pd.date_range(min(df_date[COL_NAME]), max(df_date[COL_NAME]),freq='H').strftime('%Y/%m/%d %H:%M:%S') # implementation of the date column 'DATE_ENREG' with atomicity at the hour level
    df_date = df_date.merge(df_autocomplete, how='outer', on=[COL_NAME]).fillna(0) # Merge counts by date, if it does not exissts, count equal to zero (to avoid missing hours due to missing data)
    df_date = df_date.sort_values(by=[COL_NAME]) # DataFrame sorted by dates
    df_date['EffCC'] = df_date['Eff'].cumsum() # increasing cumulative headcount
    df_date[COL_NAME] = pd.to_datetime(df_date[COL_NAME], format='%Y/%m/%d %H:%M:%S') # column formatted as timestamps
    
    
    df_date[COL_NAME_H] = df_date[COL_NAME].dt.strftime('%Y/%m/%d %H:00:00') # creation of the hours table
    df_H = df_date.groupby([COL_NAME_H], as_index=False).agg({'Eff': sum, 'EffCC':max}) # merge
    df_H['EffCC_Freq'] = round((df_H['EffCC'] / max(df_H['EffCC']))*100, 2) # creation of the column of cumulative counts increasing in percentage
    df_H[COL_NAME_H] = pd.to_datetime(df_H[COL_NAME_H], format='%Y/%m/%d %H:%M:%S') # column formatted as timestamps MEAE : %d/%m/%Y %H:%M:%S
    return df_H


if __name__ == "__main__":
    pass



