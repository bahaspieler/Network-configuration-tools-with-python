from time import time
start= time()
import pandas as pd
import os

input= pd.read_excel('input.xlsx', index_col=False)
sitename= input['Site'].to_list()


serial_3g = ['site', 'RNCName', 'rncid', 'Cell ID', 'Location Area Code', 'Routing Area Code', 'Downlink UARFCN', 'Uplink UARFCN'
             , 'DL Primary Scrambling Code']

serial_2g= ['CELLNAME', 'BSC', 'CI', 'LAC', 'BCCHNO','NCC', 'BCC']

print("ipwave reading...")
ipwave= pd.read_excel('ipwave.xlsx', sheet_name='Service-2G3G',index_col=False, skiprows=5)
final= ipwave.loc[(ipwave['SITE_NAME'].isin(sitename)) & (ipwave['SERVICE_TYPE']=='4G')]




print("dump_2g reading...")
dump_2g_main = pd.read_excel('dump.xlsx', sheet_name='BSC DUMP',index_col=False)
print("dump_3g reading...")
dump_3g_main = pd.read_excel('dump.xlsx', sheet_name='Total 3G',index_col=False)
print("CDD reading...")
cdd_main = pd.read_excel('cdd_3.xlsx', sheet_name='CDD',index_col=False)
print("L2U reading...")
lu_main= pd.read_excel('cdd_3.xlsx', sheet_name='L2U',index_col=False)
print("L2G reading...")
lg_main= pd.read_excel('cdd_3.xlsx', sheet_name='L2G',index_col=False)


for y in sitename:
    try:
        os.mkdir('{}/'.format(y))
    except:
        print("Directory exist")
    final2= final[final['SITE_NAME'].isin([y])]
    tac = final2['LAC'].astype('int64').values[0]
    cdd= cdd_main[cdd_main['Site'].isin([y])]
    cdd['cell_ext'] = cdd['LTECELLNAME'].str[-1:]
    cdd['eutrancellid'] = cdd['eNB']*256+cdd['Cell ID(*)']
    cdd['tac'] = tac


    cdd = cdd[cdd['cell_ext'].isin(['A', 'B', 'C'])]
    print(cdd)
    cell_id= cdd['Cell ID(*)'].to_list()


    lu= lu_main[lu_main['Site'].isin([y])]

    lg= lg_main[lg_main['Site'].isin([y])]









    lg_lte= lg['LTE CELL'].to_list()
    lg_nbr= lg['NBR CELL'].to_list()
    lu_lte= lu['LTE CELL'].to_list()
    lu_nbr= lu['NBR CELL'].to_list()

    print(len(lu_nbr), len(lu_lte))

    dump_2g= dump_2g_main[dump_2g_main['CELLNAME'].isin(lg_nbr)]
    dump_3g = dump_3g_main[dump_3g_main['site'].isin(lu_nbr)]
    dump_3g['rncid'] = dump_3g['RNCName'].str[-2:]



    dump_3g= dump_3g[serial_3g]
    dump_2g= dump_2g[serial_2g]

    print("For loop starting")

    list_nbr_3g=[]

    rnc_unique= dump_3g.rncid.unique()
    print(rnc_unique)

    for i in range(len(lu_nbr)):
        a= dump_3g[dump_3g['site'].isin([lu_nbr[i]])].values.flatten().tolist()
        if a==[]:
            print('Neighbour not found in dump')
        ci_df= cdd[cdd['LTECELLNAME'].isin([lu_lte[i]])]
        if ci_df.empty == False:
            ci=ci_df['Cell ID(*)'].to_list()
            lte_cell_index = ci_df['LTE CELLINDEX'].astype('int64').to_list()

            b= [lu_lte[i]]+ci+lte_cell_index+a
            list_nbr_3g.append(b)

    print("2nd loop started")
    list_nbr_2g = []

    for i in range(len(lg_nbr)):
        a= dump_2g[dump_2g['CELLNAME'].isin([lg_nbr[i]])].values.flatten().tolist()
        ci_df = cdd[cdd['LTECELLNAME'].isin([lg_lte[i]])]
        if ci_df.empty == False:
            ci = ci_df['Cell ID(*)'].to_list()
            b = [lg_lte[i]] + ci + a
            list_nbr_2g.append(b)

    print(list_nbr_3g)
    print(len(list_nbr_3g))
    print(len(lu_nbr), len(lu_lte))
    print(list_nbr_2g)




    str=[]

    print("Writing.....")
    for cell, lte_ci,lte_cell_index, site, rnc, rncid, ci, lac, rac, dl, ul, psc in list_nbr_3g:
        a= 'ADD UTRANEXTERNALCELL:MCC="470",MNC="01",RNCID={0},CELLID={1},UTRANDLARFCN={2},UTRANULARFCNCFGIND=NOT_CFG,UTRANFDDTDDTYPE=UTRAN_FDD,RACCFGIND=CFG,RAC={3},' \
           'PSCRAMBCODE={4},LAC={5},CELLNAME="{6}";'.format(rncid, ci, dl, rac, psc, lac,site)

        str.append(a)
        str.append('\n')

    for i in cell_id:
        a= 'ADD UTRANNFREQ:LOCALCELLID={0},UTRANDLARFCN=10638,UTRANFDDTDDTYPE=UTRAN_FDD,UTRANULARFCNCFGIND=NOT_CFG,' \
           'CELLRESELPRIORITYCFGIND=CFG,CELLRESELPRIORITY=4,CONNFREQPRIORITY=1;'.format(i)
        str.append(a)
        str.append('\n')

    for cell, lte_ci,lte_cell_index, site, rnc, rncid, ci, lac, rac, dl, ul, psc in list_nbr_3g:
        a='ADD UTRANNCELL:LOCALCELLID={0},MCC="470",MNC="01",RNCID={1},CELLID={2},LOCALCELLNAME="{3}",NEIGHBOURCELLNAME="{4}";'.format(lte_ci, rncid, ci, cell, site)
        str.append(a)
        str.append('\n')

    for cell, lte_ci, nbr_cell, bsc, ci, lac, bcchno, ncc, bcc in list_nbr_2g:
        a= 'ADD GERANEXTERNALCELL:MCC="470",MNC="01",GERANCELLID={0},LAC={1},RACCFGIND=NOT_CFG,' \
           'BANDINDICATOR=GSM_dcs1800,GERANARFCN={2},NETWORKCOLOURCODE=3,BASESTATIONCOLOURCODE=3,CELLNAME="{3}";'.format(ci, lac, bcchno, nbr_cell)
        str.append(a)
        str.append('\n')
    for cell, lte_ci, nbr_cell, bsc, ci, lac, bcchno, ncc, bcc in list_nbr_2g:

        a='ADD GERANNFREQGROUP:LOCALCELLID={0},BCCHGROUPID=0,GERANVERSION=GSM,STARTINGARFCN={1},' \
          'BANDINDICATOR=GSM_dcs1800,CELLRESELPRIORITYCFGIND=CFG,CELLRESELPRIORITY=3,' \
          'PMAXGERANCFGIND=NOT_CFG,THRESHXHIGH=6,CONNFREQPRIORITY=1;'.format(lte_ci, bcchno)
        str.append(a)
        str.append('\n')

    for cell, lte_ci, nbr_cell, bsc, ci, lac, bcchno, ncc, bcc in list_nbr_2g:
        a='ADD GERANNCELL:LOCALCELLID={0},MCC="470",MNC="01",LAC={1},GERANCELLID={2},' \
          'LOCALCELLNAME="{3}",NEIGHBOURCELLNAME="{4}";'.format(lte_ci,lac, ci, cell, nbr_cell)
        str.append(a)
        str.append('\n')


    with open('{}\\node_end.txt'.format(y), 'w') as f:
        f.writelines(str)


    # RNC end

    lte_cell = cdd['LTECELLNAME'].to_list()
    enodeb= cdd['eNB'].to_list()
    pci= cdd['PCI'].to_list()
    local_cell_id= cdd['Cell ID(*)'].to_list()
    lte_index = cdd['LTE CELLINDEX'].astype('int64').to_list()
    eutrancellid =cdd['eutrancellid'].to_list()
    tac_id = cdd['tac'].to_list()

    new_cdd_tuple = list(zip(lte_cell,enodeb, pci, local_cell_id, lte_index, eutrancellid, tac_id))
    new_cdd = [list(elem) for elem in new_cdd_tuple]
    print(new_cdd)




    for i in rnc_unique:
        rnc_end = []
        for l_cell, enb, phyci, local_ci, l_index, eutran, tac_i in new_cdd:
            a= 'ADD ULTECELL:LTECELLINDEX={0},LTECELLNAME="{1}",EUTRANCELLID={2},' \
               'MCC="470",MNC="01",TAC={3},CNOPGRPINDEX=0,CELLPHYID={4},LTEBAND=3,LTEARFCN=1547;'.format(l_index, l_cell, eutran, tac_i, phyci)
            rnc_end.append(a)
            rnc_end.append('\n')

        nbr_3g_filtered = dump_3g[dump_3g['rncid'].isin([i])]
        list_nbr_3g_filtered=[]

        for x in range(len(lu_nbr)):
            bool= nbr_3g_filtered[nbr_3g_filtered['site'].isin([lu_nbr[x]])]
            if bool.empty ==False:

                a = nbr_3g_filtered[nbr_3g_filtered['site'].isin([lu_nbr[x]])].values.flatten().tolist()

                ci_df = cdd[cdd['LTECELLNAME'].isin([lu_lte[x]])]
                if ci_df.empty == False:
                    ci = ci_df['Cell ID(*)'].to_list()
                    lte_cell_index = ci_df['LTE CELLINDEX'].astype('int64').to_list()

                    b = [lu_lte[x]] + ci + lte_cell_index + a
                    list_nbr_3g_filtered.append(b)
        print(list_nbr_3g_filtered)
        for cell, lte_ci, lte_cell_index, site, rnc, rncid, ci, lac, rac, dl, ul, psc in list_nbr_3g_filtered:
            a='ADD ULTENCELL:RNCID={0},CELLID={1},LTECELLINDEX={2};'.format(rncid, ci,lte_cell_index)
            rnc_end.append(a)
            rnc_end.append('\n')

        for cell, lte_ci, lte_cell_index, site, rnc, rncid, ci, lac, rac, dl, ul, psc in list_nbr_3g_filtered:
            a='ADD UCELLHOCOMM:CELLID={},' \
              'FASTRETURNTOLTESWITCH=PERFENH_PS_FAST_RETURN_LTE_SWITCH-1&HO_UMTS_TO_LTE_FAST_RETURN_SWITCH-1;'.format(ci)
            rnc_end.append(a)
            rnc_end.append('\n')

        for cell, lte_ci, lte_cell_index, site, rnc, rncid, ci, lac, rac, dl, ul, psc in list_nbr_3g_filtered:
            a='MOD UCELLHOCOMM:CellId={},U2LBLINDREDIRSWITCH=OFF,FASTRETURNTOLTESWITCH=PERFENH_PS_FAST_RETURN_LTE_SWITCH-1&HO_UMTS_TO_LTE_FAST_RETURN_SWITCH-1&HO_SRVCC_FAST_RETURN_TO_LTE_SWITCH-0&HO_CSFB_BASED_MEAS_FAST_RETURN_SWITCH-0&HO_CSFB_BASED_RSCP_FAST_RETURN_SWITCH-0&HO_CSFB_BASED_GRID_FAST_RETURN_SWITCH-0,' \
              'U2LLTELOADSWITCH=LOAD_BASE_U2L_LTE_LOAD_SWITCH-0&SERVICE_BASE_U2L_LTE_LOAD_SWITCH-0,' \
              'PENALTYTIMERFORCMFAILCOV=10;'.format(ci)
            rnc_end.append(a)
            rnc_end.append('\n')

        for cell, lte_ci, lte_cell_index, site, rnc, rncid, ci, lac, rac, dl, ul, psc in list_nbr_3g_filtered:
            a='MOD UCELLSELRESEL:CELLID={},QUALMEAS=CPICH_ECNO,IDLEQHYST1S=2,CONNQHYST1S=2,IDLEQHYST2S=1,CONNQHYST2S=2,TRESELECTIONS=2,QQUALMIN=-18,QRXLEVMIN=-58,QRXLEVMINEXTSUP=FALSE,MAXALLOWEDULTXPOWER=24,IDLESINTRASEARCH=5,IDLESINTERSEARCH=4,CONNSINTRASEARCH=5,CONNSINTERSEARCH=4,SSEARCHRAT=0,SPEEDDEPENDENTSCALINGFACTOR=255,INTERFREQTRESELSCALINGFACTOR=255,INTERRATTRESELSCALINGFACTOR=255,NONHCSIND=NOT_CONFIGURED,QHYST1SPCH=255,QHYST1SFACH=255,QHYST2SPCH=255,QHYST2SFACH=255,TRESELECTIONSPCH=255,TRESELECTIONSFACH=255,SPRIORITY=4,THDPRIORITYSEARCH1=2,THDPRIORITYSEARCH2=2,THDSERVINGLOW=1,THDSERVINGLOW2=2,PRIORESELECTSWITCH=UTRAN_RESELECT_SWITCH-0,CELLFACHPRIORESELSWITCH=OFF,CELLFACHMEASLAYER=HIGH_PRIO_LAYERS,TRIGTIME1AFORSIB=D0,' \
              'TRIGTIME1DFORSIB=D0,HYSTFOR1AFORSIB=0,HYSTFOR1DFORSIB=8,INTRARELTHD1AFORSIB=6;'.format(ci)
            rnc_end.append(a)
            rnc_end.append('\n')

        for cell, lte_ci, lte_cell_index, site, rnc, rncid, ci, lac, rac, dl, ul, psc in list_nbr_3g_filtered:
            a='MOD UCELLSIBSWITCH:CellId={}, SibCfgBitMap=SIB19-1;'.format(ci)
            rnc_end.append(a)
            rnc_end.append('\n')

        for cell, lte_ci, lte_cell_index, site, rnc, rncid, ci, lac, rac, dl, ul, psc in list_nbr_3g_filtered:
            a='ADD UCELLNFREQPRIOINFO:CellId={},EARFCN=1547,NPriority=6,ThdToHigh=6,ThdToLow=10,EMeasBW=D25,EQrxlevmin=-64,' \
              'EDetectInd=TRUE,BlacklstCellNumber=D0;'.format(ci)
            rnc_end.append(a)
            rnc_end.append('\n')

        for cell, lte_ci, lte_cell_index, site, rnc, rncid, ci, lac, rac, dl, ul, psc in list_nbr_3g_filtered:
            a='MOD UCELLNFREQPRIOINFO:CellId={},EARFCN=1547,BLACKLSTCELLNUMBER=D0,EDETECTIND=TRUE,EMEASBW=D50,EQQUALMINOFFSET=20,EQQUALMINSTEP=5,EQRXLEVMIN=-64,EQRXLEVMINOFFSET=40,EQRXLEVMINSTEP=10,FREQUSEPOLICYIND=BOTH,NPRIORITY=6,NPRIORITYCONNECT=6,' \
              'RSRQSWITCH=FALSE,SLAVEBANDINDICATOR=D0,SUPCNOPGRPINDEX=FALSE' \
              ',THDTOHIGH=6,THDTOLOW=10;'.format(ci)
            rnc_end.append(a)
            rnc_end.append('\n')

        for cell, lte_ci, lte_cell_index, site, rnc, rncid, ci, lac, rac, dl, ul, psc in list_nbr_3g_filtered:
            a='ADD UCELLU2LTEHONCOV:CELLID={},BESTCELLTRIGLTEMEASSWITCH=OFF,HYSTFOR3C=4,LTEMEASQUANOF3C=RSRP,LTEMEASTYPOF3C=MEASUREMENTQUANTITY,TARGETRATTHDRSRP=36,TARGETRATTHDRSRQ=20,TRIGTIME3C=D0,U2LGRIDINFOHIGHTHD=99,U2LGRIDINFOLOWTHD=1,U2LNCOVRSCPTHD=-90,U2LSERVALGOSWITCH=HO_GRID_BASED_LTE_SERVICE_PS_OUT_SWITCH-0&HO_LTE_SERVICE_BLIND_FIRST_SWITCH-0&HO_LTE_SERVICE_NEED_RSCP_SWITCH-0&HO_LTE_SERVICE_PSHO_OUT_SWITCH-0&HO_LTE_SERVICE_PS_OUT_SWITCH-1,U2LSERVTRIGSOURCE=U2L_SERV_IUCS_REL_TRIGGER-0&U2L_SERV_LOWACTIVE_TRIGGER-1&U2L_SERV_OTHER_TRIGGER-0&U2L_SERV_PERIOD_TRIGGER-0&U2L_SERV_RAB_SETUP_TRIGGER-0&U2L_SERV_RB_REL_TRIGGER-0,U2LTEFILTERCOEF=D3,' \
              'U2LTEMEASTIME=5;'.format(ci)
            rnc_end.append(a)
            rnc_end.append('\n')

        for cell, lte_ci, lte_cell_index, site, rnc, rncid, ci, lac, rac, dl, ul, psc in list_nbr_3g_filtered:

            a='MOD UCELLU2LTEHONCOV:CELLID={},BESTCELLTRIGLTEMEASSWITCH=OFF,HYSTFOR3C=4,LTEMEASQUANOF3C=RSRP,LTEMEASTYPOF3C=MEASUREMENTQUANTITY,TARGETRATTHDRSRP=36,TARGETRATTHDRSRQ=20,TRIGTIME3C=D0,U2LGRIDINFOHIGHTHD=99,U2LGRIDINFOLOWTHD=1,U2LNCOVRSCPTHD=-90,U2LSERVALGOSWITCH=HO_GRID_BASED_LTE_SERVICE_PS_OUT_SWITCH-0&HO_LTE_SERVICE_BLIND_FIRST_SWITCH-0&HO_LTE_SERVICE_NEED_RSCP_SWITCH-0&HO_LTE_SERVICE_PSHO_OUT_SWITCH-0&HO_LTE_SERVICE_PS_OUT_SWITCH-1,U2LSERVTRIGSOURCE=U2L_SERV_IUCS_REL_TRIGGER-0&U2L_SERV_LOWACTIVE_TRIGGER-1&U2L_SERV_OTHER_TRIGGER-0&U2L_SERV_PERIOD_TRIGGER-0&U2L_SERV_RAB_SETUP_TRIGGER-0&U2L_SERV_RB_REL_TRIGGER-0,' \
              'U2LTEFILTERCOEF=D3,U2LTEMEASTIME=5;'.format(ci)
            rnc_end.append(a)
            rnc_end.append('\n')
        with open('{0}\\rnc_{1}.txt'.format(y,i), 'w') as f:
            f.writelines(rnc_end)


    # bsc end

    bsc_end=[]
    for l_cell, enb, phyci, local_ci, l_index, eutran, tac_i in new_cdd:
        a='ADD GEXTLTECELL:EXTLTECELLNAME="{0}",MCC="470",MNC="01",ENODEBTYPE=MACRO,CI={1},TAC={2},FREQ=1547,PCID={3},' \
          'EUTRANTYPE=FDD,OPNAME="Grameenphone";'.format(l_cell, eutran, tac_i, phyci)
        bsc_end.append(a)
        bsc_end.append('\n')

    for cell, lte_ci, nbr_cell, bsc, ci, lac, bcchno, ncc, bcc in list_nbr_2g:
        a='ADD GLTENCELL:IDTYPE=BYNAME,SRCLTENCELLNAME="{0}",NBRLTENCELLNAME="{1}",SPTRESEL=SUPPORT;'.format(nbr_cell, cell)
        bsc_end.append(a)
        bsc_end.append('\n')

    for cell, lte_ci, nbr_cell, bsc, ci, lac, bcchno, ncc, bcc in list_nbr_2g:
        a='MOD GLTENCELL:IDTYPE=BYNAME,SRCLTENCELLNAME="{0}",NBRLTENCELLNAME="{1}",SPTRESEL=SUPPORT,SPTRAPIDSEL=SUPPORT;'.format(nbr_cell,cell)
        bsc_end.append(a)
        bsc_end.append('\n')

    for cell, lte_ci, nbr_cell, bsc, ci, lac, bcchno, ncc, bcc in list_nbr_2g:
        a='SET GCELLHOBASIC:IDTYPE=BYNAME,CELLNAME="{0}",LTECELLRESELEN=YES;\n' \
          'SET GCELLPRIEUTRANSYS:IDTYPE=BYNAME,CELLNAME="{0}",BESTEUTRANCELLNUM=2,EUTRANFREQCNUM=1,EUTRANPRI=6,EUTRANQRXLEVMIN=6,EUTRANRESELECTOPTSW=OFF;\n' \
          'SET GCELLPRIEUTRANSYS:IDTYPE=BYNAME,CELLNAME="{0}",THRGSMLOW=0,THRPRISEARCH=15,THRUTRANHIGH=2,THRUTRANLOW=2,TRESEL=0,UTRANPRI=4,UTRANQRXLEVMIN=2;\n' \
          'SET GCELLPRIEUTRANSYS:IDTYPE=BYNAME,CELLNAME="{0}",QPEUTRAN=15,SI2QUATEROPTFORLTESW=ON,TDDFASTRETURNRSRPTH=28,TDDLTEOFFSET=0,THREUTRANHIGH=6,THREUTRANLOW=14,THREUTRANRPT=0;\n' \
          'SET GCELLPRIEUTRANSYS:IDTYPE=BYNAME,CELLNAME="{0}",FASTRETURNFILTERSW=OFF,FASTRETURNMEASSPT=OFF,FDDFASTRETURNRSRPTH=24,FDDLTEOFFSET=0,GERANPRI=3,HPRIO=0;\n' \
          'SET GCELLSOFT:IDTYPE=BYNAME,CELLNAME="{0}",SUPPORTCSFB=SUPPORT;\n' \
          'MOD GLTENCELL:IDTYPE=BYNAME,SRCLTENCELLNAME="{0}",NBRLTENCELLNAME="{1}",SPTRESEL=SUPPORT,SPTRAPIDSEL=SUPPORT;'.format(nbr_cell,cell)
        bsc_end.append(a)
        bsc_end.append('\n')

    with open('{}\\bsc_end.txt'.format(y), 'w') as f:
        f.writelines(bsc_end)


    #field script

    GATEWAY_IP_ADDRESS_PLD =final2['GATEWAY_IP_ADDRESS_PLD'].values[0]
    PAYLOAD_BTS_LOCAL_IP_ADDRESS = final2['PAYLOAD_BTS_LOCAL_IP_ADDRESS'].values[0]
    VLAN_ID_PLD =final2['VLAN_ID_PLD'].values[0]
    ENODEBID= enodeb[0]
    RSI = cdd['RSI'].to_list()
    PB = cdd['Pb'].to_list()

    RS_POWER=cdd['RS Power(dBm)']*10
    RS_POWER= RS_POWER.astype('int64')

    field_cdd_tuple = list(zip(lte_cell, pci, RSI, local_cell_id, PB, RS_POWER))
    field_cdd = [list(elem) for elem in field_cdd_tuple]

    field_script=[]

    one= 'ADD APP:AID=3,AT=eNodeB,AN="eNodeB",APPMNTMODE=NORMAL;\n' \
         'ADD ENODEBFUNCTION:ENODEBFUNCTIONNAME="{0}L",APPLICATIONREF=3,ENODEBID={1};\n' \
         'ADD BRD:SN=2,BT=UBBP,BBWS=GSM-1&UMTS-0&LTE_FDD-1&LTE_TDD-0&NBIOT-0;\n' \
         'ADD DEVIP:SN=7,SBT=BASE_BOARD,PT=ETH,PN=0,IP="{2}",MASK="255.255.255.248",USERLABEL="LTE";\n' \
         'ADD VLANMAP:NEXTHOPIP="{3}",MASK="255.255.255.248",VLANMODE=SINGLEVLAN,VLANID={4},SETPRIO=DISABLE;\n' \
         'ADD SRCIPRT:SRCRTIDX=40,SN=7,SBT=BASE_BOARD,SRCIP="{2}",RTTYPE=NEXTHOP,NEXTHOP="{3}",' \
         'USERLABEL="LTE";\n'.format(y,ENODEBID,PAYLOAD_BTS_LOCAL_IP_ADDRESS,GATEWAY_IP_ADDRESS_PLD,VLAN_ID_PLD)

    field_script.append(one)
    field_script.append('\n')

    for l, p, r, c, pb, rs_p in field_cdd:

        two= 'ADD CELL:LOCALCELLID={0},CELLNAME="{1}",NBCELLFLAG=FALSE,FREQBAND=3,ULEARFCNCFGIND=NOT_CFG,' \
             'DLEARFCN=1547,ULBANDWIDTH=CELL_BW_N50,DLBANDWIDTH=CELL_BW_N50,CELLID={0},PHYCELLID={2},FDDTDDIND=CELL_FDD,' \
             'EUCELLSTANDBYMODE=ACTIVE,ROOTSEQUENCEIDX={3},CUSTOMIZEDBANDWIDTHCFGIND=NOT_CFG,EMERGENCYAREAIDCFGIND=NOT_CFG,' \
             'UEPOWERMAXCFGIND=NOT_CFG,MULTIRRUCELLFLAG=BOOLEAN_FALSE,TXRXMODE=2T2R;'.format(c,l,p,r)

        field_script.append(two)
        field_script.append('\n')

    three= 'ADD SECTOREQM:SECTOREQMID=20,SECTORID=1,ANTCFGMODE=ANTENNAPORT,ANTNUM=2,ANT1CN=0,ANT1SRN=180,ANT1SN=0,ANT1N=R0A,ANTTYPE1=RXTX_MODE,ANT2CN=0,ANT2SRN=180,ANT2SN=0,ANT2N=R0B,ANTTYPE2=RXTX_MODE;\n' \
           'ADD SECTOREQM:SECTOREQMID=21,SECTORID=2,ANTCFGMODE=ANTENNAPORT,ANTNUM=2,ANT1CN=0,ANT1SRN=182,ANT1SN=0,ANT1N=R0A,ANTTYPE1=RXTX_MODE,ANT2CN=0,ANT2SRN=182,ANT2SN=0,ANT2N=R0B,ANTTYPE2=RXTX_MODE;\n' \
           'ADD SECTOREQM:SECTOREQMID=22,SECTORID=3,ANTCFGMODE=ANTENNAPORT,ANTNUM=2,ANT1CN=0,ANT1SRN=184,ANT1SN=0,ANT1N=R0A,ANTTYPE1=RXTX_MODE,ANT2CN=0,ANT2SRN=184,ANT2SN=0,ANT2N=R0B,ANTTYPE2=RXTX_MODE;'

    field_script.append(three)
    field_script.append('\n')

    four='ADD EUCELLSECTOREQM:LOCALCELLID=11,SECTOREQMID=20,CELLBEAMMODE=NORMAL;\n' \
         'ADD EUCELLSECTOREQM:LOCALCELLID=12,SECTOREQMID=21,CELLBEAMMODE=NORMAL;\n' \
         'ADD EUCELLSECTOREQM:LOCALCELLID=13,SECTOREQMID=22,CELLBEAMMODE=NORMAL;\n' \
         'ADD EPGROUP:EPGROUPID=0;\n' \
         'ADD EPGROUP:EPGROUPID=10,USERLABEL="S1";\n' \
         'ADD EPGROUP:EPGROUPID=11,USERLABEL="X2";\n' \
         'ADD SCTPHOST:SCTPHOSTID=10,IPVERSION=IPv4,SIGIP1V4="{0}",SIGIP1SECSWITCH=DISABLE,SIGIP2SECSWITCH=DISABLE,PN=36412,SIMPLEMODESWITCH=SIMPLE_MODE_OFF,SCTPTEMPLATEID=0,USERLABEL="S1";\n' \
         'ADD SCTPHOST:SCTPHOSTID=11,IPVERSION=IPv4,SIGIP1V4="{0}",SIGIP1SECSWITCH=DISABLE,SIGIP2SECSWITCH=DISABLE,PN=36422,SIMPLEMODESWITCH=SIMPLE_MODE_OFF,SCTPTEMPLATEID=0,USERLABEL="X2";\n' \
         'ADD SCTPPEER:SCTPPEERID=10,IPVERSION=IPv4,SIGIP1V4="10.177.55.10",SIGIP1SECSWITCH=DISABLE,SIGIP2SECSWITCH=DISABLE,PN=36412,SIMPLEMODESWITCH=SIMPLE_MODE_OFF;\n' \
         'ADD SCTPPEER:SCTPPEERID=11,IPVERSION=IPv4,SIGIP1V4="10.176.55.10",SIGIP1SECSWITCH=DISABLE,SIGIP2SECSWITCH=DISABLE,PN=36412,SIMPLEMODESWITCH=SIMPLE_MODE_OFF;\n' \
         'ADD SCTPPEER:SCTPPEERID=12,IPVERSION=IPv4,SIGIP1V4="10.175.55.10",SIGIP1SECSWITCH=DISABLE,SIGIP2SECSWITCH=DISABLE,PN=36412,SIMPLEMODESWITCH=SIMPLE_MODE_OFF;\n' \
         'ADD SCTPTEMPLATE:SCTPTEMPLATEID=0,SWITCHBACKFLAG=ENABLE;\n' \
         'ADD USERPLANEHOST:UPHOSTID=0,IPVERSION=IPv4,LOCIPV4="10.2.21.139",IPSECSWITCH=DISABLE,USERLABEL="3G_P_IP";\n' \
         'ADD USERPLANEHOST:UPHOSTID=10,IPVERSION=IPv4,LOCIPV4="{0}",IPSECSWITCH=DISABLE,USERLABEL="S1X2";\n' \
         'ADD UPHOST2EPGRP:EPGROUPID=0,UPHOSTID=0;\n' \
         'ADD UPHOST2EPGRP:EPGROUPID=10,UPHOSTID=10;\n' \
         'ADD UPHOST2EPGRP:EPGROUPID=11,UPHOSTID=10;\n' \
         'ADD UPPEER2EPGRP:EPGROUPID=0,UPPEERID=0;\n' \
         'ADD UPPEER2EPGRP:EPGROUPID=0,UPPEERID=1;\n' \
         'ADD USERPLANEPEER:UPPEERID=0,IPVERSION=IPv4,PEERIPV4="10.177.226.2",IPSECSWITCH=DISABLE,USERLABEL="RNCIP";\n' \
         'ADD USERPLANEPEER:UPPEERID=1,IPVERSION=IPv4,PEERIPV4="10.177.226.1",IPSECSWITCH=DISABLE,USERLABEL="RNCIP";\n' \
         'ADD CNOPERATOR:CNOPERATORID=0,CNOPERATORNAME="GP",CNOPERATORTYPE=CNOPERATOR_PRIMARY,MCC="470",MNC="01",OPERATORFUNSWITCH=CELL_TRAFFIC_TRACE_MSG_SWITCH-1;\n' \
         'ADD CNOPERATORTA:TRACKINGAREAID=0,CNOPERATORID=0,TAC={1};\n' \
         'ADD S1:S1ID=0,CNOPERATORID=0,EPGROUPCFGFLAG=CP_UP_CFG,CPEPGROUPID=10,UPEPGROUPID=10,USERLABEL="LTE";\n' \
         'ADD CELLOP:LOCALCELLID=11,TRACKINGAREAID=0,MMECFGNUM=CELL_MME_CFG_NUM_0;\n' \
         'ADD CELLOP:LOCALCELLID=12,TRACKINGAREAID=0,MMECFGNUM=CELL_MME_CFG_NUM_0;\n' \
         'ADD CELLOP:LOCALCELLID=13,TRACKINGAREAID=0,MMECFGNUM=CELL_MME_CFG_NUM_0;'.format(PAYLOAD_BTS_LOCAL_IP_ADDRESS,tac)

    field_script.append(four)
    field_script.append('\n')

    for l, p, r, c, pb, rs_p in field_cdd:
        five='MOD PDSCHCFG:LOCALCELLID={0},REFERENCESIGNALPWR={1},PB={2};'.format(c,rs_p,pb)
        field_script.append(five)
        field_script.append('\n')

    six= 'ADD SCTPPEER2EPGRP:EPGROUPID=10,SCTPPEERID=10;\n' \
         'ADD SCTPPEER2EPGRP:EPGROUPID=10,SCTPPEERID=11;\n' \
         'ADD SCTPPEER2EPGRP:EPGROUPID=10,SCTPPEERID=12;\n' \
         'ADD SCTPHOST2EPGRP:EPGROUPID=10,SCTPHOSTID=10;\n' \
         'ADD SCTPHOST2EPGRP:EPGROUPID=11,SCTPHOSTID=11;\n' \
         'ADD S1:S1ID=0,CNOPERATORID=0,EPGROUPCFGFLAG=CP_UP_CFG,CPEPGROUPID=10,UPEPGROUPID=10,USERLABEL="LTE";\n'
    field_script.append(six)
    with open('{}\\field_script.txt'.format(y), 'w') as f:
        f.writelines(field_script)

end= time()

print("time elapsed: ", (end-start)/60)