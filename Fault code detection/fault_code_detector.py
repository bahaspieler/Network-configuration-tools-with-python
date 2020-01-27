print('* Copyright (C) Baha Uddin Ahmed- All Rights Reserved\n* Proprietary and confidential\n* For any query <baha.uar1994@gmail.com>\n* Created in 18 November, 2019\n----------------------------------------------------------\n')
print("N.B:- Keep your input file name as 'fault_code.txt' \n")
import re
from timeit import default_timer as timer

text= open(r'fault_code.txt', encoding='utf-8')

contents= text.read()

alarm= input('Please insert the alarm text:- ')



# p1= re.compile(r'(MO\s+RESULT\s+TFMODE\s+[A-Z\s]+\n)([A-Z]+-\d+)([A-Z\s\d-]*)(HFS REDUCED DUE TO SPECTRUM SHARING)')

# p1= re.compile(r'(\*\*\* Connected to CGEBS04 \*\*\*\n)([<\WA-Z=\-;\d\s]+)(MO\s+RESULT\s+TFMODE\s+[A-Z\s]+\n)(RXSTF-1678)([A-Z\s\d-]*)(HFS REDUCED DUE TO SPECTRUM SHARING)')
#
# m1= p1.findall(contents)

p1 = re.compile(r'(\*\*\* Connected to )(\w+)( \*\*\*)')
m1 = p1.findall(contents)



list_m1= list(zip(*m1))

del list_m1[0]
del list_m1[1]

print(list_m1)

bsc_list= [list(ele) for ele in list_m1]
bsc= bsc_list[0]
print(len(bsc))

p2= re.compile(r'(MO\s+RESULT\s+TFMODE\s+[A-Z\s]+\n)([A-Z]+-\d+)([A-Z\s\d-]*)({0})'.format(alarm))
m2= p2.findall(contents)

list_tup= list(zip(*m2))

del list_tup[0]
del list_tup[1:3]


tg_list= [list(ele) for ele in list_tup]
tg_dup= tg_list[0]
tg= list(dict.fromkeys(tg_dup))
print(len(tg_dup))
print(len(tg))

print('number of tg', len(tg))

# cme=0
# if cme == len(bsc)-1:
#     cme=0
#
# length = len(tg)-1
#
# for i in range(length):
#     p3 = re.compile(r'(\*\*\* Connected to {0} \*\*\*\n)([<\WA-Z=\-;\d\s]+)(MO\s+RESULT\s+TFMODE\s+[A-Z\s]+\n)({1})([A-Z\s\d-]*)(HFS REDUCED DUE TO SPECTRUM SHARING)'.format(bsc[cme], tg[i]))
#     m3 = p3.findall(contents)
#
#     if len(m3)==0:
#         cme+=1
#         i-=1
#
#
#     print(m3)
#     print(bsc[cme])


print("<<--WAIT.....Getting done-->>")
final=[]

start= timer()


another = []


for i in tg:
    for x in bsc:
        p3 = re.compile(
            r'(\*\*\* Connected to {0} \*\*\*\n)([<\WA-Z=\-;\d\s]+)(MO\s+RESULT\s+TFMODE\s+[A-Z\s]+\n)({1})([A-Z\s\d-]*)({2})'.format(
                x, i, alarm))
        m3 = p3.findall(contents)

        if len(m3) != 0:
            # f= i+"-"+x
            final.append(i + '-' + x)
            final.append('\n')
            # print(i,"is in:-",x)
            break

        else:
            pass

end= timer()

with open("bsc_tg.txt", 'w') as g:
    g.writelines(final)
print("time taken:- ", end-start)
input("<<---PRESS ENTER TO EXIT--->>")

