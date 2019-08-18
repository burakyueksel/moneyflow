#!/usr/bin/env python
'''
author: burak yuksel
'''
from lib_readCSVSparda import *
from lib_report import*
from fpdf import FPDF
from PIL import Image
import os

# row data, subracted from the online bank webpage is stored here
filename = 'test.csv'

# get the big_data from the row data
big_data = return_CSV_data_sparda(filename)

# post process and organize the big_data
transaction_time_window_overall_s, current_saldo_f, \
    date_array_booking_s, date_array_transaction_s, info_array_s, amount_array_f, saldo_array_f = big_data_organizer_sparda(big_data)

# order of this classification is important.
# Considering there are n elements in this class vector,
# first n-1 elements shall be all some sort of costs.
# n-th element shall always be the income.

# FIXME: remove class_vector and go with the first column of class_matrix
class_vector = ('grocery', 
                'insurance', 
                'com_int', 
                'health', 
                'transport', 
                'house',
                'cash', 
                'sport', 
                'creditcard', 
                'charity', 
                'income')

#                       class           keywords
class_matrix        = (('grocery',      ['REWE','ALNATURA','NATURGUT','DM','EDEKA','DENNS','Drogeriemarkt Muller','NETTO','LIDL','flaschenpost','SCHECK-IN','KAUFHOF','BAUHAUS','NORMA','MARKTLADEN']),
                       ('insurance',    ['DEBEK','VERSICHERUNG','versicherung','Rente','Swiss Life','DFV']),
                       ('com_int',      ['UNITYMEDIA','TCHIBO MOBIL','NETFLIX','Rundfunk']),
                       ('health',       ['APOTHEKE']),
                       ('transport',    ['DB Vertrieb','Bus','LOGPAY','StadtMobil CarSharing','RNV']),
                       ('house',        ['EnBW','Stadtwerk','MIETE','VERENA VOLK']),
                       ('cash',         ['BBBANK','60090800 GAA','KartenumsatzCardProcess','VOLKSBANK','SANTANDER']),
                       ('sport',        ['SCHWIMM','CAFE KRAFT','BOULDERHAUS','BOULDERHAL']),
                       ('creditcard',   ['MASTERCARD']),
                       ('charity',      ['Arbeiter-Samariter-Bund']),
                       ('income',       ['ITK','Retina Implant','RETINA','VOLOCOPTER','VIBROSONIC'])
)
# class_matrix[:][0][0] -> 'grocery'
# class_matrix[:][1][0] -> 'insurance'
# class_matrix[:][2][0] -> 'com_int'
# class_matrix[:][i][0] ->  class
#
# class_matrix[0][1][:] -> ['REWE','ALNATURA','NATURGUT','DM','EDEKA','DENNS','Drogeriemarkt Muller']
# class_matrix[1][1][:] -> ['DEBEK','VERSICHERUNG','versicherung','Rente','Swiss Life','DFV']
# class_matrix[2][1][:] -> ['UNITYMEDIA','TCHIBO MOBIL','NETFLIX']
# class_matrix[i][1][:] -> [keywords]
'''
    per element of the classification, following loop generates and initializes:
    - an info array for storing the information of relevant transaction
    - an index array for storing the index of the element in big_data
    - a float for summing up the costs/incomes of the element over big_data
'''
#create_data_struct(classifications)
for element in class_vector:
    #exec ("%s = %f" % (element+'_array',1.0))
    vars()[element+'_array']=[]
    vars()[element+'_indexes']=[]
    vars()[element+'_amounts']=0.0

# init other variables
found_cost_indexes      = []
notfound_costs_indexes  = []
notfound_income_indexes = []

# write info_array to a file
write_to_file_owerwrite(info_array_s,'infos.txt')

'''
# experimenting: factorize the following code for writing all amounts etc to the specific classes.
for info in info_array_s:
    for i in range(len(class_matrix)-1):
        if any(keyword in info for keyword in class_matrix[0][1][:]):
            vars()[class_matrix[:][i][0]+'_amounts'], vars()[class_matrix[:][i][0]+'_array'], vars()[class_matrix[:][i][0]+'_indexes'], found_cost_indexes = \
            cost_organizer(info, info_array_s, amount_array_f, vars()[class_matrix[:][i][0]+'_amounts'], \
            vars()[class_matrix[:][i][0]+'_array'], vars()[class_matrix[:][i][0]+'_indexes'], found_cost_indexes)
'''
# search keywords in information array for classificaton
for info in info_array_s:
    if any(keyword in info for keyword in class_matrix[0][1][:]):
        grocery_amounts, grocery_array, grocery_indexes, found_cost_indexes = \
            cost_organizer(info, info_array_s, amount_array_f, grocery_amounts, \
                grocery_array, grocery_indexes, found_cost_indexes)
    if any(keyword in info for keyword in class_matrix[1][1][:]):
        insurance_amounts, insurance_array, insurance_indexes, found_cost_indexes = \
            cost_organizer(info, info_array_s, amount_array_f, insurance_amounts, \
                insurance_array, insurance_indexes, found_cost_indexes)
    if any(keyword in info for keyword in class_matrix[2][1][:]):
        com_int_amounts, com_int_array, com_int_indexes, found_cost_indexes = \
            cost_organizer(info, info_array_s, amount_array_f, com_int_amounts, \
                com_int_array, com_int_indexes, found_cost_indexes)
    if any(keyword in info for keyword in class_matrix[3][1][:]):
        health_amounts, health_array, health_indexes, found_cost_indexes = \
            cost_organizer(info, info_array_s, amount_array_f, health_amounts, \
                health_array, health_indexes, found_cost_indexes)        
    if any(keyword in info for keyword in class_matrix[4][1][:]):
        transport_amounts, transport_array, transport_indexes, found_cost_indexes = \
            cost_organizer(info, info_array_s, amount_array_f, transport_amounts, \
                transport_array, transport_indexes, found_cost_indexes)  
    if any(keyword in info for keyword in class_matrix[5][1][:]):
        house_amounts, house_array, house_indexes, found_cost_indexes = \
            cost_organizer(info, info_array_s, amount_array_f, house_amounts, \
                house_array, house_indexes, found_cost_indexes)
    if any(keyword in info for keyword in class_matrix[6][1][:]):
        cash_amounts, cash_array, cash_indexes, found_cost_indexes = \
            cost_organizer(info, info_array_s, amount_array_f, cash_amounts, \
                cash_array, cash_indexes, found_cost_indexes)
    if any(keyword in info for keyword in class_matrix[7][1][:]):
        sport_amounts, sport_array, sport_indexes, found_cost_indexes = \
            cost_organizer(info, info_array_s, amount_array_f, sport_amounts, \
                sport_array, sport_indexes, found_cost_indexes)
    if any(keyword in info for keyword in class_matrix[8][1][:]):
        creditcard_amounts, creditcard_array, creditcard_indexes, found_cost_indexes = \
            cost_organizer(info, info_array_s, amount_array_f, creditcard_amounts, \
                creditcard_array, creditcard_indexes, found_cost_indexes)
    if any(keyword in info for keyword in class_matrix[9][1][:]):
        charity_amounts, charity_array, charity_indexes, found_cost_indexes = \
            cost_organizer(info, info_array_s, amount_array_f, charity_amounts, \
                charity_array, charity_indexes, found_cost_indexes)
    # incomes
    if any(keyword in info for keyword in class_matrix[10][1][:]):
        income_array.append(info)
        income_indexes.append( info_array_s.index(info))

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

plotter(all_costs, all_incomes, grocery_amounts, insurance_amounts, com_int_amounts, health_amounts, \
                    transport_amounts, house_amounts, cash_amounts, sport_amounts, creditcard_amounts, charity_amounts,\
                    total_notfound_cost_amounts, transaction_time_window_overall_s)

path_to_plots = '/mnt/c/Users/buyue/code/moneyflow/plots'
path_to_pdf   = filename+'report.pdf'
reporter(path_to_plots,path_to_pdf,messages)

