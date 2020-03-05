print('\n\n* Copyright (C) Baha Uddin Ahmed- All Rights Reserved\n* Proprietary and confidential\n* For any query <baha.cuet13@gmail.com>\n* Created in 04 February, 2020\n----------------------------------------------------------\n')


import pandas as pd
import re
import os

work_type= int(input("\n> Please insert the type of work(Choose from the below options:)\nMGW = 1\nMSS = 2\nMGW+MSS = 3\n"))



def find_missing(list_f):
    return [x for x in range(list_f[0], list_f[-1]+1)
                               if x not in list_f]

def ranges(nums):
    nums = sorted(set(nums))
    gaps = [[s, e] for s, e in zip(nums, nums[1:]) if s+1 < e]
    edges = iter(nums[:1] + sum(gaps, []) + nums[-1:])
    return list(zip(edges, edges))


def groupSequence(lst):
    res = [[lst[0]]]

    for i in range(1, len(lst)):
        if lst[i - 1] + 1 == lst[i]:
            res[-1].append(lst[i])

        else:
            res.append([lst[i]])
    return res


#--------------------------


txt_dir=[f for f in os.listdir('input') if f.endswith(".txt")]

print('\n> Text files found: ',txt_dir)

backup_mss=[]
icx_mgw = []


for i in txt_dir:
    # p1= re.compile("(icx|ICX|Icx|MGW|mgw|Mgw)")
    # p2 = re.compile("(mss|MSS|Mss|backup|Backup|BACKUP)")
    p1 = re.compile("icx|mgw", re.IGNORECASE)
    p2 = re.compile("mss", re.IGNORECASE)

    if work_type == 1 or work_type==3:
        if p1.findall(i):
            icx_mgw.append("input\\{}".format(i))
    if work_type == 2 or work_type==3:
        if p2.findall(i):
            backup_mss.append("input\\{}".format(i))




xl_dir= ["input\\{}".format(f) for f in os.listdir("input") if f.endswith(".xls") and "$" not in f]
print('\n> Plan file: ', xl_dir)

p1= re.compile(r'[A-Z]+[0-9]+')

p2= re.compile(r'(\d+)(\s+\w+\-\w+\s+)(\s+H\'\w+\s+)([A-Za-z]+\s+)(H\'\w+\s+\d+\s+)([A-Za-z]+\s+[A-Za-z]+\s+)([A-Za-z]+\s+[A-Za-z]+\s+[A-Za-z]+\s+)')


plan = pd.read_excel(xl_dir[0], index_col=False)
a1= plan.columns[0]

#names from a1
m1= p1.findall(a1)


# name part

name = 'T{0}W{1}-{2}'.format(m1[0][-2:], m1[1][-2:], m1[2])
print('\n> Name: ',name)

# decimal to hex part


print("\n> reading plan....")
plan2= pd.read_excel(xl_dir[0], index_col=False, usecols='M,N', nrows=6)

origin_dec_str = plan2.iloc[0,1]
origin = hex(int(origin_dec_str.split('-')[1])).split('x')[-1].upper()
print('\n> Origin: ',origin)

dest_dec_str = plan2.iloc[2,1]
dest = hex(int(dest_dec_str.split('-')[1])).split('x')[-1].upper()
print('\n> Destination: ',dest)
# main string output block
full_block_a =[]


if work_type == 1 or work_type == 3:
    text = open(icx_mgw[0], 'r', encoding='utf-8')
    contents = text.read()

    m2 = p2.findall(contents)

    m2_list1= list(zip(*m2))


    n7dsp_index_str = list(m2_list1[0])


    n7dsp_index_int= [int(x) for x in n7dsp_index_str]


    n7dsp_index_missing= find_missing(n7dsp_index_int)
    print('\n> Missing Index Values: ',n7dsp_index_missing)


    if n7dsp_index_missing == []:
        n7dsp_index = n7dsp_index_int[-1]+1


    else:
        n7dsp_index = n7dsp_index_missing[0]

    print('\n> Index found: ',n7dsp_index)
    # ospindex

    pattern_osp= re.compile(r'(\d+)(\s+\w+\s+\w+\s+\w+\s+H\')({})'.format(origin))
    match_osp = pattern_osp.findall(contents)



    match_osp_tup= list(zip(*match_osp))
    match_osp_list = list(match_osp_tup[0])
    # got ospindex here
    osp_ind= [int(x) for x in match_osp_list][0]
    print('\n> OSP index: ',osp_ind)

    # osp_origin= list(match_osp_tup[2])
    #
    # print(osp_origin)

    # finding slc






    slc_search= [(plan[col][plan[col].eq('SLC')].index[i], plan.columns.get_loc(col)) for col in plan.columns for i in range(len(plan[col][plan[col].eq('SLC')].index))]
    slc_loc = slc_search[0][0]
    type= [(plan[col][plan[col].eq('Type')].index[i], plan.columns.get_loc(col)) for col in plan.columns for i in range(len(plan[col][plan[col].eq('Type')].index))]
    type_loc = type[0][0]

    plan_slc= pd.read_excel(xl_dir[0], index_col=False, skiprows=slc_loc+1).dropna(how='all')
    plan_type= pd.read_excel(xl_dir[0], index_col=False, skiprows=type_loc+1).dropna(how='all')

    slc= plan_slc['SLC'].dropna(how='any').astype('int64').to_list()
    print('\n> SLC: ', slc)
    link_to_be_add = 0

    if 0 in slc:
        link_to_be_add+=1
    if 1 in slc:
        link_to_be_add+=1
    if 2 in slc:
        link_to_be_add+=1
    if 3 in slc:
        link_to_be_add+=1


    print('\n> Link to be added: ',link_to_be_add)

    # linkno

    pattern_linkno= re.compile(r'(\d+)(\s+\w+\-\w+\-\d+\s+\w+_\w+)')

    match_linkno = pattern_linkno.findall(contents)

    match_linkno_tup= list(zip(*match_linkno))
    match_linkno_str = list(match_linkno_tup[0])

    match_linkno_int= [int(x) for x in match_linkno_str]

    linkno_missing = find_missing(match_linkno_int)
    print('\n> Link no missing values: ',linkno_missing)

    linkno =[]
    link_name= []
    if linkno_missing == []:
        for a in range(link_to_be_add):
            linkno.append(match_linkno_int[-1]+(a+1))
            link_name.append(name+'-{}'.format(a+1))

    else:
        linkno_missing_group = groupSequence(linkno_missing)
        print(linkno_missing_group)
        for i in linkno_missing_group:
            if len(i) >= link_to_be_add:
                linkno= i[:(link_to_be_add)]
                for j in range(len(linkno)):
                    link_name.append(name+'-{}'.format(j+1))


    print('\n> Linkno',linkno)
    print('\n> Link Name: ',link_name)

    # IFBT-IFBN , port/opn

    ifbt_ifbn = plan_type['Type'].to_list()[0].split('-')
    opn= int(plan_type['Port'].to_list()[0])
    print('\n> OPN: ',opn)
    print('\n> IFBT IFBN: ',ifbt_ifbn)



    block_a= "ADD N7DSP: INDEX= {0} , NAME=\"{1}\", NI=NAT, DPC=H'{2}, OSPINDEX= {3} , NETTYPE=STDSG;\n" \
             "ADD N7LKS: INDEX= {0} , NAME=\"{1}\", DSPIDX= {0} ;\n" \
             "ADD N7RT: INDEX= {0} , NAME=\"{1}\", LKSIDX= {0}, DSPIDX= {0};\n\n".format(n7dsp_index, name, dest, osp_ind )
    full_block_a.append(block_a)

    for i in slc:
        if i == 0 or i ==2:
            block_b= "ADD MTP2LNK: LNKNO={5}, LNKNAME=\"{0}\", IFBT={1}, IFBN={2}, OPN={3}, E1T1N={4}, STRTTS=***, ENDTS=***, SPFBN=***, SUBBN=***, LNKTYPE=MTP***K;\n" \
                     "ADD N7LNK: INDEX={5}, NAME=\"{0}\", LKSIDX={6}, SLC=***, MTP2NO={5};\n\n".format(link_name[i], ifbt_ifbn[0], ifbt_ifbn[1], opn, 0, linkno[i], n7dsp_index)
        if i == 1 or i == 3:
            block_b = "ADD MTP2LNK: LNKNO={5}, LNKNAME=\"{0}\", IFBT={1}, IFBN={2}, OPN={3}, E1T1N={4}, STRTTS=***, ENDTS=***, SPFBN=***, SUBBN=***, LNKTYPE=MTP***K;\n" \
                      "ADD N7LNK: INDEX={5}, NAME=\"{0}\", LKSIDX={6}, SLC=1, MTP2NO={5};\n\n".format(link_name[i], ifbt_ifbn[0],
                                                                                                 ifbt_ifbn[1], opn, 1,linkno[i], n7dsp_index)
        full_block_a.append(block_b)

else:
    print("\n> MGW input taken")



if work_type == 3 or work_type == 2:
    mss_backup = open(backup_mss[0], 'r', encoding='utf-8')
    mss_content = mss_backup.read()

    lenm_pattern = re.compile(r'(Local entity name  =\s+)([\w_]+)')
    lenm_match = lenm_pattern.findall(mss_content)
    lenm= lenm_match[0][1]
    print('\n> LENM: ', lenm)

    lsnm_pattern = re.compile(r'(Destination entity name  =\s+)([\w_]+)')
    lsnm_match = lsnm_pattern.findall(mss_content)
    lsnm= lsnm_match[0][1]
    print('\n> LSNM: ', lsnm)

    mscn_pattern =re.compile(r'(\d+\s+\d+\s+)(880\d+)(\s+[A-Z]+\s+)')
    mscn_match = mscn_pattern.findall(mss_content)
    mscn= mscn_match[0][1]
    print('\n> MSCN: ', mscn)

    tid_search= [(plan[col][plan[col].eq('EQM(NEW)')].index[i], plan.columns.get_loc(col)) for col in plan.columns for i in range(len(plan[col][plan[col].eq('EQM(NEW)')].index))]


    tid_loc =tid_search[0][0]
    plan_tid= pd.read_excel(xl_dir[0], index_col=False, skiprows=tid_loc+1).dropna(how='all')
    tid_list =list(plan_tid['EQM(NEW)'].dropna())

    tid= [int(i[4:])*32 for i in tid_list]
    print('\n> TID: ', tid)

    #bofcn part

    lst_ofc_pattern= re.compile(r'Office direction name  =  \w+')
    lst_ofc_match = lst_ofc_pattern.findall(mss_content)
    print('\n> LST OFC output: ',lst_ofc_match)

    if lst_ofc_match ==[]:

        bofcn_pattern = re.compile(r'(H\'\w+\s+)(MSC\s+)(\s+[A-Za-z]+\s+)([A-Za-z\s]+)(\s+)([A-Za-z\s]+)(\s+)(\d+)')
        bofcn_match= bofcn_pattern.findall(mss_content)

        match_bofcn_tup= list(zip(*bofcn_match))

        match_bofcn_list = sorted([int(i) for i in list(match_bofcn_tup[-1])])
        print('\n> Existing BOFCN: ', match_bofcn_list)
        # print(match_bofcn_list)

        btg_pattern= re.compile(r'(H\'\w+\s+H\'\w+\s+)([A-Za-z\s]+)([A-Za-z\s]+)([A-Za-z\s]+)(\d+\s+)(\d+)')
        btg_match = btg_pattern.findall(mss_content)

        match_btg_tup= list(zip(*btg_match))
        match_btg_list = sorted([int(i) for i in list(match_btg_tup[-1])])
        print('\n> Existing BTG: ', match_btg_list)

        blank_bofcn = find_missing(match_bofcn_list)
        print('\n> Blank BOFCN: ', blank_bofcn)
        blank_btg= find_missing(match_btg_list)
        print('\n> Blank BTG: ', blank_btg)

        bofcn_btg= [i for i in blank_btg if i in blank_bofcn and 780>=i>=750][0]

        print('\n> Final BOFCN_BTG: ', bofcn_btg)


    if m1[2][3:5] == 'DH':
        rssn = 'DHK'
    elif m1[2][3:5] == 'KH':
        rssn = 'KHL'
    elif m1[2][3:5] == 'BO':
        rssn = 'BOG'
    elif m1[2][3:5] == 'CG':
        rssn = 'CTG'
    elif m1[2][3:5] == 'SY':
        rssn = 'SYL'

    print('\n> RSSN: ', rssn)

    mgwname_pattern= re.compile(r'([A-Z]+{0})(\s+\d+\s+)([A-Za-z\s]+)(\s+\d+)([A-Za-z\s]+)(\s+[A-Z]+{0})'.format(m1[1][-3:]))
    mgwname_match= mgwname_pattern.findall(mss_content)
    print('\n> MGWNAME: ',mgwname_match[0][0])

    if lst_ofc_match == []:
        block_c= 'ADD M3DE: DENM="{0}", LENM="{1}", NI=NAT, DPC="{2}", DET=SP;\n' \
                 'ADD M3RT: RTNM="{0}", DENM="{0}", LSNM="{3}";\n' \
                 'ADD CALLSRC: CSCNAME="{0}", P=***,RSSN="{4}", FSN="***", INNAME="INVALID", AC="***", MSCN=K\'{5};\n' \
                 'ADD OFC: ON="{0}", OOFFICT=MSC, DOL=HIGH, DOA=MSC, BOFCNO={6}, OFCTYPE=COM, SIG=NONBICC/NONSIP, NI=NAT, DPC1="{2}";\n' \
                 'ADD BILLCTRL: OFFICENAME="{0}", OOFFICT=OTHERNET;\n' \
                 'MOD BILLCTRL: OFFICENAME="{0}", OOFFICT=OTHERNET, GWIGENERATE=YES, GWOGENERATE=YES;\n' \
                 'ADD SRT: SRN="{7}", ON="{0}", ACC1="INVALID", ACC2="INVALID", BFSM=INVALID;\n' \
                 'ADD N7TG: TGN="{7}", MGWNAME="{8}", CT=ISUP,CSM=MAX, CSCNAME="{0}", SRN="{7}",BTG={6},SOPC="***", SDPC="{2}", ABT=NO, IPM=DFT, DI=K\'{5}, CC=NO, LOCNAME="INVALID", RELRED=NO;\n' \
                 'MOD N7TG: TGN="{7}",ABT=YES, NIF=NO, IPM=DFT, DI=K\'***, ISCLR=NO, ECMD=EC_ON, DISGRP=***;\n\n'.format(name, lenm, dest, lsnm, rssn, mscn, bofcn_btg, m1[2], mgwname_match[0][0])

    else:
        block_c = 'ADD M3DE: DENM="{0}", LENM="{1}", NI=NAT, DPC="{2}", DET=SP;\n' \
                  'ADD M3RT: RTNM="{0}", DENM="{0}", LSNM="{3}";\n' \
                  'ADD CALLSRC: CSCNAME="{0}", P=***,RSSN="{4}", FSN="***", INNAME="INVALID", AC="***", MSCN=K\'{5};\n' \
                  'ADD BILLCTRL: OFFICENAME="{0}", OOFFICT=OTHERNET;\n' \
                  'MOD BILLCTRL: OFFICENAME="{0}", OOFFICT=OTHERNET, GWIGENERATE=YES, GWOGENERATE=YES;\n' \
                  'ADD SRT: SRN="{6}", ON="{0}", ACC1="INVALID", ACC2="INVALID", BFSM=INVALID;\n' \
                  'ADD N7TG: TGN="{6}", MGWNAME="{7}", CT=ISUP,CSM=MAX, CSCNAME="{0}", SRN="{6}",BTG={6},SOPC="***", SDPC="{2}", ABT=NO, IPM=DFT, DI=K\'{5}, CC=NO, LOCNAME="INVALID", RELRED=NO;\n' \
                  'MOD N7TG: TGN="{6}",ABT=YES, NIF=NO, IPM=DFT, DI=K\'***, ISCLR=NO, ECMD=EC_ON, DISGRP=***;\n\n'.format(
            name, lenm, dest, lsnm, rssn, mscn, m1[2], mgwname_match[0][0])


    full_block_a.append(block_c)

    block_d=[]

    scic=0
    ecic= 31

    for i in tid:
        block_d_a='ADD N7TKC:TGN="{0}",SCIC={1},ECIC={2},TID={3};\n'.format(m1[2], scic, ecic, i)
        full_block_a.append(block_d_a)
        scic+=32
        ecic+=32


if work_type==1:

    with open("{}_MGW.txt".format(name), 'w') as f:
        f.writelines(full_block_a)

elif work_type==2:
    with open("{}_MSS.txt".format(name), 'w') as f:
        f.writelines(full_block_a)

else:
    with open("{}.txt".format(name), 'w') as f:
        f.writelines(full_block_a)