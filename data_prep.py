"""
Created on Thu Jan 17 11:18:23 2019
@author:
Performing data preparation tasks on available data.
"""

import pandas as pd


# Data Preparation ASN Crypto Exchange Platforms
items = pd.read_csv('./crosschecked.csv')
items_asn2 = pd.DataFrame(items.asn2)
items_asn = pd.DataFrame(items.asn)
items_asn2.rename(columns = {'asn2':'asn'}, inplace = True)
items = pd.concat([items_asn2,items_asn])
items = items[items.asn != 0]
items.drop_duplicates(inplace=True)
items.to_csv("./items.csv", index = False, header = False)



# Data Preparation CAIDA Data
edgelist = pd.read_csv('./Edgelist', sep = "	",header = None)
edgelist.rename(columns = {0:'from',1:'to'}, inplace = True)

rows = []
for index,row in edgelist.iterrows():
    if '_' in str(row['from']):
        splittedRows = row['from'].split('_')
        for i in splittedRows:
            new_row = row.to_dict()
            new_row['from'] = i
            rows.append(new_row)
    else:
        new_row = row.to_dict()
        rows.append(new_row)
edgelist = pd.DataFrame(rows)

rows = []
for index,row in edgelist.iterrows():
    if '_' in str(row['to']):
        splittedRows = row['to'].split('_')
        for i in splittedRows:
            new_row = row.to_dict()
            new_row['to'] = i
            rows.append(new_row)
    else:
        new_row = row.to_dict()
        rows.append(new_row)
edgelist = pd.DataFrame(rows)

for index,row in edgelist.iterrows():
    if '_' in str(row['from']) or '_' in str(row['to']):
        print(row)
    elif ',' in str(row['from']) or ',' in str(row['to']):
        print(row)

edgelist.to_csv("./Edgelist_clean.txt", index = False, header = False, sep = "	")