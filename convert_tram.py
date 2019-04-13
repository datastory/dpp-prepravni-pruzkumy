#%%
import pandas as pd
import os

#%%
def reader_tram(file):
    with open(file, 'r', encoding='windows-1250') as f:
        data = f.read().replace('\n', '')

    #%%
    # zahození komentářů
    data = data[14:]
    data = data.split('$')[0]
    data = data.split(';')

    #%%
    header_cnt = int(data[16]) # počet hlaviček
    record_cnt = int(data[17]) # počet záznamů

    #%%
    headers = []
    cursor = 18 + 4 # před hlavičkami je 4x nerelevatní hodnota
    while cursor < (header_cnt * 11) + 22:
        headers.append(data[cursor : cursor + 11])
        cursor += 11

    #%%
    records = []
    cursor = (header_cnt * 11) + 22 # všechny hodnoty před hlavičkami a hlavičky
    while cursor < (record_cnt * 19) + (header_cnt * 11) + 22:
        records.append(data[cursor : cursor + 19])
        cursor += 19

    #%%
    h = pd.DataFrame.from_dict(headers)
    h = h.applymap(lambda x: x.replace('"', ''))
    cols = [
        'ID spoje',
        'Počáteční datum',
        'Koncové datum'
    ]
    cols.extend(range(1, 9))
    h.columns = cols
    h.to_csv('data_csv/' + file.split('/')[-1].split('.')[0] + '_headers.csv', encoding='utf-8', index=False)

    #%%
    r = pd.DataFrame.from_dict(records)
    r = r.applymap(lambda x: x.replace('"', ''))
    cols = [
        'ID spoje',
        'ID záznamu',
        'Skutečný odjezd',
        'Plánovaný odjezd',
        'Skutečný příjezd',
        'Plánovaný příjezd',
        'Nástupy1',
        'Nástupy2',
        'PočetPoNástupu1',
        'PočetPoNástupu2',
        'PočetPředVýstupem1',
        'PočetPředVýstupem2',
        'Výstupy1',
        'Výstupy2',
        'Číslo uzlu zastávky',
        'Číslo sloupku zastávky',
        'Číslo linky',
        'Pořadí zastávky na trase',
        'Flags'
    ]
    r.columns = cols
    r.to_csv('data_csv/' + file.split('/')[-1].split('.')[0] + '_records.csv', encoding='utf-8', index=False)

#%% convert TRAM
for f in os.listdir('data'):
    if f.startswith('TRAM'):
        reader_tram('data/' + f)