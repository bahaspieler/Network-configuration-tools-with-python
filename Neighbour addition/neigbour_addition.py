import pandas as pd
import re
import os




xl_dir= [f for f in os.listdir() if f.endswith(".xlsx") and "$" not in f]
print(xl_dir)

one= []
two =[]
three= []


for i in xl_dir:
    p1= re.compile("(2g|2G).(2g|2G)")
    p2= re.compile("(3g|3G).(2g|2G)")
    p22= re.compile("(2g|2G).(3g|3G)")
    p3 = re.compile("(3g|3G).(3g|3G)")


    if p1.findall(i):
        one.append(i)
    if p2.findall(i):
        two.append(i)
    if p22.findall(i):
        two.append(i)
    if p3.findall(i):
        three.append(i)

print(one,'\n', two, '\n', three, '\n')

print("Reading dump file...\n")
dump = pd.read_excel('Nei add dump.xlsx', sheet_name='BSC DUMP', index_col=False, usecols='A,B,E:I')
dump2= pd.read_excel('Nei add dump.xlsx', sheet_name='Total 3G',index_col=False, usecols='A:E,G:J')



if len(one)==1:
    print("2G-2G script generation process started..\n")
    plan = pd.read_excel(one[0], index_col=False)



    source_cell_id = plan['Source 2G Cell ID'].to_list()
    source_bsc = plan['Source BSC'].to_list()
    nei_cell_id = plan['Neighbor 2G Cell ID'].to_list()
    nei_bsc = plan['Neighbor BSC'].to_list()
    source_cell_name = plan['Source 2G Cell Name'].to_list()
    nei_cell_name = plan['Neighbor 2G Cell Name'].to_list()

    plan_tuple = list(zip(source_cell_id, source_bsc, nei_cell_id,nei_bsc,source_cell_name,nei_cell_name))
    plan_list = [list(elem) for elem in plan_tuple]

    print(plan_list)
    all_bsc = source_bsc+nei_bsc
    unique_bsc = list(set(all_bsc))


    for ub in unique_bsc:
        open('output\\{}_2g_2g.txt'.format(ub), 'w')

    print('entering the for loop')


    for sci, sb, nci, nb, scn, ncn in plan_list:
        if sb == nb:
            a = 'ADD G2GNCELL:IDTYPE=BYNAME,SRC2GNCELLNAME="{0}",NBR2GNCELLNAME="{1}",NCELLTYPE=HANDOVERNCELL,SRCHOCTRLSWITCH=HOALGORITHM1;\n' \
              'ADD G2GNCELL:IDTYPE=BYNAME,SRC2GNCELLNAME="{1}",NBR2GNCELLNAME="{0}",NCELLTYPE=HANDOVERNCELL,SRCHOCTRLSWITCH=HOALGORITHM1;\n'.format(scn,ncn)
            with open('output\\{}_2g_2g.txt'.format(sb), 'a') as f:
                f.write(a)


        if sb != nb:
            info_b = dump[dump['CELLNAME'].isin([ncn])].values.flatten().tolist()
            info_c= dump[dump['CELLNAME'].isin([scn])].values.flatten().tolist()

            print(info_b)
            b = 'ADD GEXT2GCELL:EXT2GCELLNAME="{0}",MCC="470",MNC="01",LAC={1},CI={2},BCCH={3},NCC={4},BCC={5};\n' \
               'ADD G2GNCELL:IDTYPE=BYNAME,SRC2GNCELLNAME="{6}",NBR2GNCELLNAME="{0}",NCELLTYPE=HANDOVERNCELL,' \
               'SRCHOCTRLSWITCH=HOALGORITHM1;\n'.format(ncn, info_b[2], info_b[3],info_b[6],info_b[4], info_b[5], scn)

            c = 'ADD GEXT2GCELL:EXT2GCELLNAME="{6}",MCC="470",MNC="01",LAC={1},CI={2},BCCH={3},NCC={4},BCC={5};\n' \
               'ADD G2GNCELL:IDTYPE=BYNAME,SRC2GNCELLNAME="{0}",NBR2GNCELLNAME="{6}",NCELLTYPE=HANDOVERNCELL,' \
               'SRCHOCTRLSWITCH=HOALGORITHM1;\n'.format(ncn, info_c[2], info_c[3],info_c[6],info_c[4], info_c[5], scn)

            with open('output\\{}_2g_2g.txt'.format(sb), 'a') as f:
                f.write(b)

            with open('output\\{}_2g_2g.txt'.format(nb), 'a') as f:
                f.write(c)


else:
    if len(one)==0:

        print("2G-2G plan file not found")
    if len(one)==2:
        print("Multiple 2G-2G plan file found")


if len(three)==1:
    print("\n3G-3G script generation process started..\n")
    plan2 = pd.read_excel(three[0], index_col=False)


    source_3g_cell_id = plan2['Source 3G Cell ID'].to_list()
    source_rnc= plan2['Source RNC'].to_list()
    source_rnc_id =plan2['Source RNC'].str[-2:].astype('int64').to_list()
    print(source_rnc_id)
    nei_3g_cell_id = plan2['Neighbor 3G Cell ID'].to_list()
    nei_rnc = plan2['Neighbor RNC'].to_list()
    nei_rnc_id = plan2['Neighbor RNC'].str[-2:].astype('int64').to_list()
    print(nei_rnc_id)
    source_3g_cell = plan2['Source 3G Cell Name'].to_list()
    nei_3g_cell = plan2['Neighbor 3G Cell Name'].to_list()

    plan2_tuple = list(zip(source_3g_cell_id, source_rnc,source_rnc_id, nei_3g_cell_id, nei_rnc, nei_rnc_id, source_3g_cell, nei_3g_cell))
    plan2_list = [list(elem) for elem in plan2_tuple]
    print(plan2_list)
    all_rnc = source_rnc + nei_rnc
    unique_rnc = list(set(all_rnc))

    for ub in unique_rnc:
        open('output\\{}_3g_3g.txt'.format(ub), 'w')

    for sci, sr,sri, nci, nr, nri, scn, ncn in plan2_list:
        if sri == nri:
            a= 'ADD UINTRAFREQNCELL:RNCID={0},CELLID={1},NCELLRNCID={0},NCELLID={2},SIB11IND=TRUE,SIB12IND=FALSE,TPENALTYHCSRESELECT=D0,NPRIOFLAG=FALSE;\n' \
               'ADD UINTRAFREQNCELL:RNCID={0},CELLID={2},NCELLRNCID={0},NCELLID={1},SIB11IND=TRUE,SIB12IND=FALSE,' \
               'TPENALTYHCSRESELECT=D0,NPRIOFLAG=FALSE;\n'.format(sri, sci, nci )


            with open('output\\{}_3g_3g.txt'.format(sr), 'a') as f:
                f.write(a)

        if sri != nri:
            info_b = dump2[dump2['site'].isin([ncn])].values.flatten().tolist()
            info_c = dump2[dump2['site'].isin([scn])].values.flatten().tolist()
            print(info_b)

            b= 'ADD UEXT3GCELL:NRNCID={0},CELLID={1},CELLHOSTTYPE=SINGLE_HOST,CELLNAME="{2}",CNOPGRPINDEX=0,PSCRAMBCODE={3},BANDIND=Band1,UARFCNUPLINKIND=TRUE,' \
               'UARFCNUPLINK={4},UARFCNDOWNLINK={5},TXDIVERSITYIND=FALSE,LAC={6},CFGRACIND=REQUIRE,RAC={7},QQUALMININD=FALSE,QRXLEVMININD=FALSE,MAXALLOWEDULTXPOWERIND=FALSE,USEOFHCS=NOT_USED,CELLCAPCONTAINERFDD=HSDSCH_SUPPORT-1&FDPCH_SUPPORT-1&EDCH_SUPPORT-1&EDCH_2MS_TTI_SUPPORT-1&EDCH_2SF2_AND_2SF4_SUPPORT-0&EDCH_2SF2_SUPPORT-0&EDCH_2SF4_SUPPORT-1&EDCH_SF4_SUPPORT-0&EDCH_SF8_SUPPORT-0&EDCH_HARQ_IR_COMBIN_SUPPORT-1&EDCH_HARQ_CHASE_COMBIN_SUPPORT-1&CPC_DTX_DRX_SUPPORT-0&CPC_HS_SCCH_LESS_OPER_SUPPORT-0&HSPAPLUS_MIMO_SUPPORT-0&FLEX_MACD_PDU_SIZE_SUPPORT-0&FDPCH_SLOT_FORMAT_SUPPORT-0&HSPAPLUS_DL_64QAM_SUPPORT-0,EFACHSUPIND=FALSE;\n' \
               'ADD UINTRAFREQNCELL:RNCID={8},CELLID={9},NCELLRNCID={0},NCELLID={1},SIB11IND=TRUE,SIB12IND=FALSE,' \
               'TPENALTYHCSRESELECT=D0,NPRIOFLAG=FALSE;\n'.format(nri, nci, ncn, info_b[5], info_b[3], info_b[4], info_b[6],info_b[8], sri, sci,nri)

            c = 'ADD UEXT3GCELL:NRNCID={8},CELLID={9},CELLHOSTTYPE=SINGLE_HOST,CELLNAME="{2}",CNOPGRPINDEX=0,PSCRAMBCODE={3},BANDIND=Band1,UARFCNUPLINKIND=TRUE,' \
                'UARFCNUPLINK={4},UARFCNDOWNLINK={5},TXDIVERSITYIND=FALSE,LAC={6},CFGRACIND=REQUIRE,RAC={7},QQUALMININD=FALSE,QRXLEVMININD=FALSE,MAXALLOWEDULTXPOWERIND=FALSE,USEOFHCS=NOT_USED,CELLCAPCONTAINERFDD=HSDSCH_SUPPORT-1&FDPCH_SUPPORT-1&EDCH_SUPPORT-1&EDCH_2MS_TTI_SUPPORT-1&EDCH_2SF2_AND_2SF4_SUPPORT-0&EDCH_2SF2_SUPPORT-0&EDCH_2SF4_SUPPORT-1&EDCH_SF4_SUPPORT-0&EDCH_SF8_SUPPORT-0&EDCH_HARQ_IR_COMBIN_SUPPORT-1&EDCH_HARQ_CHASE_COMBIN_SUPPORT-1&CPC_DTX_DRX_SUPPORT-0&CPC_HS_SCCH_LESS_OPER_SUPPORT-0&HSPAPLUS_MIMO_SUPPORT-0&FLEX_MACD_PDU_SIZE_SUPPORT-0&FDPCH_SLOT_FORMAT_SUPPORT-0&HSPAPLUS_DL_64QAM_SUPPORT-0,EFACHSUPIND=FALSE;\n' \
                'ADD UINTRAFREQNCELL:RNCID={0},CELLID={1},NCELLRNCID={8},NCELLID={9},SIB11IND=TRUE,SIB12IND=FALSE,' \
                'TPENALTYHCSRESELECT=D0,NPRIOFLAG=FALSE;\n'.format(nri, nci, scn, info_c[5], info_c[3], info_c[4],
                                                                 info_c[6], info_c[8], sri, sci)

            with open('output\\{}_3g_3g.txt'.format(sr), 'a') as f:
                f.write(b)

            with open('output\\{}_3g_3g.txt'.format(nr), 'a') as f:
                f.write(c)

else:
    if len(three)==0:

        print("3G-3G plan file not found")
    if len(three)==2:
        print("Multiple 3G-3G plan file found")

if len(two)==1:
    print("\n3G-2G script generation process started..\n")
    plan3 = pd.read_excel(two[0], index_col=False)

    source_3g_cell_id = plan3['Source 3G Cell ID'].to_list()
    source_rnc = plan3['Source RNC'].to_list()
    source_rnc_id = plan3['Source RNC'].str[-2:].astype('int64').to_list()
    print(source_rnc_id)
    nei_2g_cell_id = plan3['Neighbor 2G Cell Index'].to_list()
    nei_bsc = plan3['Neighbor BSC'].to_list()
    source_3g_cell = plan3['Source 3G Cell Name'].to_list()
    nei_2g_cell = plan3['Neighbor 2G Cell Name'].to_list()

    plan3_tuple = list(
        zip(source_3g_cell_id, source_rnc, source_rnc_id, nei_2g_cell_id, nei_bsc, source_3g_cell,
            nei_2g_cell))
    plan3_list = [list(elem) for elem in plan3_tuple]
    print(plan3_list)

    unique_rnc = list(set(source_rnc))
    unique_bsc = list(set(nei_bsc))
    all_unique = unique_rnc+unique_bsc

    for au in all_unique:
        open('output\\{}_3g_2g.txt'.format(au), 'w')

    for sci, sr, sri, nci, nb, scn, ncn in plan3_list:
        info_a= dump2[dump2['site'].isin([scn])].values.flatten().tolist()
        info_b= dump[dump['CELLNAME'].isin([ncn])].values.flatten().tolist()
        print(info_b)

        a='ADD GEXT3GCELL:EXT3GCELLNAME="{0}",MCC="470",MNC="01",LAC={1},CI={2},RNCID={3},DF={4},SCRAMBLE={5},DIVERSITY=YES,UTRANCELLTYPE=FDD;\n' \
          'ADD G3GNCELL:IDTYPE=BYNAME,SRC3GNCELLNAME="{6}",NBR3GNCELLNAME="{0}";\n'.format(scn, info_a[6], sci, sri, info_a[4], info_a[5], ncn)

        with open('output\\{}_3g_2g.txt'.format(nb), 'a') as f:
            f.write(a)

        b='ADD UEXT2GCELL:GSMCELLINDEX={0},GSMCELLNAME="{1}",NBSCINDEX=0,LDPRDRPRTSWITCH=OFF,MCC="470",MNC="01",CNOPGRPINDEX=0,LAC={2},' \
          'CFGRACIND=NOT_REQUIRE,CID={3},NCC={4},BCC={5},BCCHARFCN={6},RATCELLTYPE=EDGE,USEOFHCS=NOT_USED,SUPPPSHOFLAG=TRUE;\n' \
          'ADD U2GNCELL:RNCID={7},CELLID={8},GSMCELLINDEX={0},BLINDHOFLAG=FALSE,NPRIOFLAG=FALSE;\n'.format(nci, ncn, info_b[2], info_b[3], info_b[4], info_b[5],
                                                                                                              info_b[6], sri, sci )

        with open('output\\{}_3g_2g.txt'.format(sr), 'a') as f:
            f.write(b)