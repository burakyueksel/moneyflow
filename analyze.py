#!/usr/bin/env python
'''
author: burak yuksel
'''
from lib_readCSVSparda import *
from lib_report import*
# from classify import *

# row data, subracted from the online bank webpage is stored here
foldername  = 'logs/'
filename    = '20190601-20200216.csv' # 20190801-20200103.csv
path_to_data= foldername + filename

# get the big_data from the row data
big_data = return_CSV_data_sparda(path_to_data)

big_data_reversed=big_data
for x in range(0,len(big_data)): big_data_reversed[x]=big_data[x][::-1]
big_data = big_data_reversed

# order of this classification is important.
# Considering there are n rows in this class matrix, i.e. len(class_matrix)=n,
# first n-1 rows shall be all some sort of costs.
# n-th row shall always be the income.
# first column is dedicated to the classes
# second column is dedicated to the keywords defining these classes
#                       class           keywords
class_matrix        = (('grocery',      ['SATURN','REWE','ALNATURA','NATURGUT','DM','EDEKA','DENNS','Drogeriemarkt Muller','NETTO','LIDL','flaschenpost','SCHECK-IN','KAUFHOF','BAUHAUS','NORMA','MARKTLADEN','SPEICHER','ROSSMANN']),
                       ('insurance',    ['DEBEK','VERSICHERUNG','versicherung','Rente','Swiss Life','DFV']),
                       ('com_int',      ['UNITYMEDIA','TCHIBO MOBIL','NETFLIX','Rundfunk']),
                       ('health',       ['APOTHEKE']),
                       ('transport',    ['DB Vertrieb','Bus','LOGPAY','StadtMobil CarSharing','RNV','Rail']),
                       ('house',        ['LENA WILLHAUCK', 'EnBW','Stadtwerk','MIETE','VERENA VOLK','KAUTION']),
                       ('cash',         ['RAIFFEISENBANK','BBBANK','60090800 GAA','KartenumsatzCardProcess','VOLKSBANK','SANTANDER','TARGOBANK']),
                       ('sport',        ['AQWA','SKI','VENICE','SCHWIMM','CAFE KRAFT','BOULDERHAUS','BOULDERHAL','ALBTHERMEN','SPORT','BOULDER']),
                       ('creditcard',   ['MASTERCARD']),
                       ('charity',      ['Arbeiter-Samariter-Bund']),
                       ('income',       ['ITK','Retina Implant','RETINA','VOLOCOPTER','VIBROSONIC'])
)
# class_matrix[:][0][0] -> 'grocery'  = class_matrix [0][0]
# class_matrix[:][1][0] -> 'insurance'= class_matrix [1][0]
# class_matrix[:][2][0] -> 'com_int'  = class_matrix [2][0]
# class_matrix[:][i][0] -> 'class'    = class_matrix [3][0]
#
# class_matrix[0][1][:] -> ['REWE','ALNATURA','NATURGUT','DM','EDEKA','DENNS','Drogeriemarkt Muller']
# class_matrix[1][1][:] -> ['DEBEK','VERSICHERUNG','versicherung','Rente','Swiss Life','DFV']
# class_matrix[2][1][:] -> ['UNITYMEDIA','TCHIBO MOBIL','NETFLIX']
# class_matrix[i][1][:] -> [keywords]

#create_data_struct(classifications)
#for element in class_vector:
   ##exec ("%s = %f" % (element+'_array',1.0))
for cnt_class in range(len(class_matrix)):
    element = class_matrix[cnt_class][0]
    vars()[element+'_array']=[]
    vars()[element+'_indexes']=[]
    vars()[element+'_amounts']=0.0

# Experimental: a better way of creating new variables automatically.
# TODO: Use this instead of vars(). This way you can push that code into another function
# without need of global definitions, e.g. using global()

'''
variables_array_names   = []
variables_indexes_names = []
variables_amounts_names = []
for cnt_class in range(len(class_matrix)):
    variables_array_names.append(class_matrix[cnt_class][0]+'_array')
    variables_indexes_names.append(class_matrix[cnt_class][0]+'_indexes')
    variables_amounts_names.append(class_matrix[cnt_class][0]+'_amounts')

import collections
variables_arrays = collections.namedtuple('Variables', variables_array_names)._make([] for _ in variables_array_names)
variables_indexes= collections.namedtuple('Variables', variables_indexes_names)._make([] for _ in variables_indexes_names)
variables_amounts= collections.namedtuple('Variables', variables_amounts_names)._make(0.0 for _ in variables_amounts_names)
'''

# init other variables
found_cost_indexes      = []
notfound_costs_indexes  = []
notfound_income_indexes = []

# cost_information, income_information, time_information = classify(big_data, class_matrix)

# post process and organize the big_data
transaction_time_window_overall_s, current_saldo_f, \
    date_array_booking_s, date_array_transaction_s, info_array_s, amount_array_f, saldo_array_f = big_data_organizer_sparda(big_data)

'''
    per row of the class_matrix, following loop generates and initializes:
    - an info array for storing the information of relevant transaction
    - an index array for storing the index of the element in big_data
    - a float for summing up the costs/incomes of the element over big_data
'''
# write info_array to a file
write_to_file_owerwrite(info_array_s,'infos.txt')

# write important in a better format to be used later if needed
write_to_file_owerwrite_summary([date_array_booking_s,date_array_transaction_s,amount_array_f,info_array_s],'summary.txt')

# factorize the following code for writing all amounts etc to the specific classes.
# search keywords in information array for classificaton
for info in info_array_s:
    for i in range(len(class_matrix)-1):
        if any(keyword in info for keyword in class_matrix[i][1][:]):
            globals()[class_matrix[:][i][0]+'_amounts'], globals()[class_matrix[:][i][0]+'_array'], globals()[class_matrix[:][i][0]+'_indexes'], found_cost_indexes = \
            cost_organizer(info, info_array_s, amount_array_f, globals()[class_matrix[:][i][0]+'_amounts'], \
            globals()[class_matrix[:][i][0]+'_array'], globals()[class_matrix[:][i][0]+'_indexes'], found_cost_indexes)
    if any(keyword in info for keyword in class_matrix[-1][1][:]):
        income_array.append(info)
        income_indexes.append( info_array_s.index(info))

# found costs and incomes
found_cost_indexes_sum = len(grocery_indexes) + len(insurance_indexes) + len(com_int_indexes) + \
      len(health_indexes) + len(transport_indexes) + len(house_indexes) + \
      len(cash_indexes) + len(sport_indexes) + \
      len(creditcard_indexes) + len(charity_indexes)
found_income_indexes = len(income_indexes)
msg = "{} % of the data is identified and classified.".format(float(found_cost_indexes_sum) /float(len(info_array_s)-found_income_indexes)*100)
print(msg)


# sum of the amounts from the identified/processed costs
total_found_cost_amounts = 0
for index in found_cost_indexes:
    total_found_cost_amounts  +=  amount_array_f[index]
# print('total found costs:', total_found_cost_amounts)

# sum of the amounts from the identified/processed incomes
total_found_income_amounts = 0
for index in income_indexes:
    total_found_income_amounts += amount_array_f[index]

# sum of the costs/incomes which are neither identified cost nor identified incomes
# also get their indices
total_notfound_cost_amounts = 0
total_notfound_income_amounts=0
for index in range(len(amount_array_f)):
    if (index not in found_cost_indexes) and (index not in income_indexes):
        # if negative, it is a cost
        if amount_array_f[index]<0:
            total_notfound_cost_amounts  += amount_array_f[index]
            notfound_costs_indexes.append(index)
        # else (0, or positive) consider it income
        else:
            total_notfound_income_amounts  +=  amount_array_f[index]
            notfound_income_indexes.append(index)

all_costs   = total_found_cost_amounts + total_notfound_cost_amounts 
all_incomes = total_found_income_amounts + total_notfound_income_amounts

# with open ('name','a') as writeFile -> this would add the data to the existing file
# +w will overwrite:
with open ('not_recognized_costs.txt', 'w+') as writeFile:
    for index in notfound_costs_indexes:
        writeFile.write(info_array_s[index]+"\n")
with open ('not_recognized_income.txt', 'w+') as writeFile:
    for index in notfound_income_indexes:
        writeFile.write(info_array_s[index]+"\n")

messages = printer(all_costs,all_incomes,current_saldo_f,saldo_array_f,transaction_time_window_overall_s)

# this is needed for generating the figures and saving them in figure folder
plotter(saldo_array_f, date_array_transaction_s,all_costs, all_incomes, grocery_amounts, insurance_amounts, com_int_amounts, health_amounts, \
                    transport_amounts, house_amounts, cash_amounts, sport_amounts, creditcard_amounts, charity_amounts,\
                    total_notfound_cost_amounts, transaction_time_window_overall_s)

path_to_plots = '/mnt/c/Users/buyue/code/moneyflow/plots'
path_to_pdf   = path_to_data+'report.pdf'
reporter(path_to_plots,path_to_pdf,messages)

