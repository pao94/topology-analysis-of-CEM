"""
Created on Sun Jan 20 15:15:30 2019
@author:
Computing a variety of graph metrics on retrieved data.
"""

import networkx as nx
import xlsxwriter
from networkx.algorithms.connectivity import local_node_connectivity
import pandas as pd


G=nx.read_edgelist("./Edgelist_clean.txt", delimiter = "\t", encoding = 'utf-8')
print (nx.info(G))

R=max(nx.connected_component_subgraphs(G), key=len)

ECC=nx.eccentricity(R)
print("Eccentricity", ECC)
eccen_df = pd.DataFrame.from_dict(ECC, orient = 'index', columns = ['ECC'])
eccen_df['AS'] = eccen_df.index
eccen_df = eccen_df[['AS','ECC']]

mean=dict()
for i in G.nodes():
    SSSPL=nx.single_source_shortest_path_length(G,source=i) 
    mean[i]= float(sum(SSSPL.values())/len(SSSPL))
print(mean)

mean_metric = pd.DataFrame.from_dict(mean, orient = 'index', columns = ['SSSPL'])
mean_metric['AS'] = mean_metric.index
mean_metric = mean_metric[['AS','SSSPL']]

workbook = xlsxwriter.Workbook('./data_SSSPL.xlsx')
worksheet = workbook.add_worksheet()

#writing into a file
print('start writing')
row = 0
col = 0
for key,value in zip (mean.keys(),mean.values()):
    worksheet.write(row,col,key)
    worksheet.write(row,col+1,value)
    row += 1    
print('done writing')
workbook.close()
print('DONE calculating SSSPL')

# calculating Degree centrality
DC=nx.degree(G)
print("Degree Centrality", DC)
degree_centrality = list(DC)
degree_centrality = pd.DataFrame(degree_centrality, columns = ['AS','DC'])
degree_centrality = degree_centrality.set_index('AS')
degree_centrality['AS'] = degree_centrality.index
degree_centrality = degree_centrality[['AS','DC']]

# calculating Eigenvector Centrality
EC=nx.eigenvector_centrality(G)
print("Eigenvector Centrality", EC)
ev_centrality = pd.DataFrame.from_dict(EC, orient = 'index', columns = ['EC'])
ev_centrality['AS'] = ev_centrality.index
ev_centrality = ev_centrality[['AS','EC']]

# calculating betweenness centrality
BC=nx.betweenness_centrality(G,normalized=True)
print("Betweennes Centrality", BC)
bc_centrality = pd.DataFrame.from_dict(BC, orient = 'index', columns = ['BC'])
bc_centrality['AS'] = bc_centrality.index
bc_centrality = bc_centrality[['AS','BC']]

# calculating closeness centrality
CLC=nx.closeness_centrality(G)
print("Closenss Centrality", CLC)
cl_centrality = pd.DataFrame.from_dict(CLC, orient = 'index', columns = ['CLC'])
cl_centrality['AS'] = cl_centrality.index
cl_centrality = cl_centrality[['AS','CLC']]


# calculating local average neighbor degree
LAND=nx.average_neighbor_degree(G)
print("Local Average Neighbor Degree", LAND)
land_df = pd.DataFrame.from_dict(LAND, orient = 'index', columns = ['LAND'])
land_df['AS'] = land_df.index
land_df = land_df[['AS','LAND']]

# calculating clustering coefficient
CC=nx.clustering(G)
print("Clustering Coefficient", CC)
cc_df = pd.DataFrame.from_dict(CC, orient = 'index', columns = ['CC'])
cc_df['AS'] = cc_df.index
cc_df = cc_df[['AS','CC']]

dfs = [degree_centrality,ev_centrality,cl_centrality,bc_centrality,eccen_df,mean_metric,land_df,cc_df]
dfs = [df.set_index('AS') for df in dfs]
allDF = dfs[0].join(dfs[1:])


writer = pd.ExcelWriter('outputMetrics.xlsx')
allDF.to_excel(writer,"Sheet1")
writer.save()



# calculating LNC for Germany (AS 3320)
workbook = xlsxwriter.Workbook('./data_35_items_LNC_GER.xlsx')
worksheet = workbook.add_worksheet()
LNC_list=dict()
#making a list of sample data
print('making a list')
data=[line.strip() for line in open("./items_all.txt",'r')]
#calculating LNC
print('Start Calculation')
for line in data:
    try:
        LNC=local_node_connectivity(G,'3320',line)
        LNC_list[line]=LNC
    except Exception as e:
        LNC_list[line] = 0
print('start writing')
row = 0
col = 0
for key,value in zip (LNC_list.keys(),LNC_list.values()):
    worksheet.write(row,col,key)
    worksheet.write(row,col+1,value)
    row += 1    
print('done writing')
workbook.close()
print('DONE calculating LNC for GER Source')

# calculating LNC for USA (AS 701)

workbook = xlsxwriter.Workbook('./data_35_items_LNC_USA.xlsx')
worksheet = workbook.add_worksheet()
LNC_list=dict()

#calculating LNC
print('Start Calculation')
for line in data:
    try:
        LNC=local_node_connectivity(G,'701',line)
        LNC_list[line]=LNC
    except Exception as e:
        LNC_list[line]= "NULL"
        
print('start writing')
row = 0
col = 0
for key,value in zip (LNC_list.keys(),LNC_list.values()):
    worksheet.write(row,col,key)
    worksheet.write(row,col+1,value)
    row += 1    
print('done writing')
workbook.close()
print('DONE calculating LNC for USA Source')

# calculating LNC for China (AS 45102)

workbook = xlsxwriter.Workbook('./data_35_items_LNC_CHN.xlsx')
worksheet = workbook.add_worksheet()
LNC_list=dict()

#calculating LNC
print('Start Calculation')
for line in data:
    try:
        LNC=local_node_connectivity(G,'45102',line)
        LNC_list[line]=LNC
    except Exception as e:
        LNC_list[line]= "NULL"
print('start writing')
row = 0
col = 0
for key,value in zip (LNC_list.keys(),LNC_list.values()):
    worksheet.write(row,col,key)
    worksheet.write(row,col+1,value)
    row += 1    
print('done writing')
workbook.close()
print('DONE calculating LNC for CHN Source')