import pandas as pd

serial_3g = ['site', 'RNCName', 'rncid', 'Cell ID', 'Location Area Code', 'Routing Area Code', 'Downlink UARFCN', 'Uplink UARFCN'
             , 'DL Primary Scrambling Code']

serial_2g= ['CELLNAME', 'BSC', 'CI', 'LAC', 'BCCHNO','NCC', 'BCC']

dump_2g = pd.read_excel('dump.xlsx', sheet_name='BSC DUMP',index_col=False)
dump_3g = pd.read_excel('dump.xlsx', sheet_name='Total 3G',index_col=False)
cdd = pd.read_excel('cdd_2.xlsx', sheet_name='CDD',index_col=False)
cdd= cdd[cdd['Site'].isin(['NPDML2'])]
cell_id= cdd['Cell ID(*)'].to_list()


lu= pd.read_excel('cdd_2.xlsx', sheet_name='L2U',index_col=False)
lu= lu[lu['Site'].isin(['NPDML2'])]
lg= pd.read_excel('cdd_2.xlsx', sheet_name='L2G',index_col=False)
lg= lg[lg['Site'].isin(['NPDML2'])]


lg_nbr= lg['NBR CELL'].to_list()
lu_lte= lg['LTE CELL'].to_list()
lu_nbr= lu['NBR CELL'].to_list()
print(len(lu_nbr))

dump_2g= dump_2g[dump_2g['CELLNAME'].isin(lg_nbr)]
dump_3g = dump_3g[dump_3g['site'].isin(lu_nbr)]
dump_3g['rncid'] = dump_3g['RNCName'].str[-2:]



dump_3g= dump_3g[serial_3g]
dump_2g= dump_2g[serial_2g]

print("For loop starting")

list_nbr_3g=[]

for i in lu_nbr:
    a= dump_3g[dump_3g['site'].isin([i])].values.flatten().tolist()
    list_nbr_3g.append(a)

print("2nd loop started")
list_nbr_2g = []

for i in lg_nbr:
    a= dump_2g[dump_2g['CELLNAME'].isin([i])].values.flatten().tolist()
    list_nbr_2g.append(a)

print(list_nbr_3g)
print(list_nbr_2g)

str=[]

print("Writing.....")
for site, rnc, rncid, ci, lac, rac, dl, ul, psc in list_nbr_3g:
    a= 'ADD UTRANEXTERNALCELL:MCC="470",MNC="01",RNCID={0},CELLID={1},UTRANDLARFCN={2},UTRANULARFCNCFGIND=NOT_CFG,UTRANFDDTDDTYPE=UTRAN_FDD,RACCFGIND=CFG,RAC={3},' \
       'PSCRAMBCODE={4},LAC={5},CELLNAME="{6}";'.format(rncid, ci, dl, rac, psc, lac,site)

    str.append(a)
    str.append('\n')

for i in cell_id:
    a= 'ADD UTRANNFREQ:LOCALCELLID={0},UTRANDLARFCN=10638,UTRANFDDTDDTYPE=UTRAN_FDD,UTRANULARFCNCFGIND=NOT_CFG,' \
       'CELLRESELPRIORITYCFGIND=CFG,CELLRESELPRIORITY=4,CONNFREQPRIORITY=1;'.format(i)
    str.append(a)
    str.append('\n')




with open('test.txt', 'w') as f:
    f.writelines(str)

