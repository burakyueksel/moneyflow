#!/usr/bin/env python
'''
author: burak yuksel
'''
def detect_date_sparda(data):
    # assumptions:
    # specific to sparda bank data
    # assumption: date is in format of dd.mm.yyyy
    # first entry (indice 0) is: " 
    # date is starting from the second (i.e. indice 1) entry of the row
    # the first entry of the row after " is always a full date
    is_date = False
    string_count=1
    for string in data:
        if string[2] is '.':
            is_date = True
            break
        string_count += 1
    return is_date

def cost_organizer(info, info_array_s, amount_array_f, cost_amounts, cost_array, cost_indexes, found_cost_indexes):
    # big_data[:][2].index(info) gives the index, in which the searched 'word's given in the if case above are found in info. big_data[:][3] has the amounts.
    cost_amounts +=  amount_array_f[ info_array_s.index(info)]
    # get all that specific cost relevant info in one array
    cost_array.append(info)
    # get the indexes of all that specific cost relevant info
    cost_indexes.append( info_array_s.index(info))
    # this is a found/identified cost. Add the index of it to the found cost indexes.
    found_cost_indexes.append( info_array_s.index(info))
    return cost_amounts, cost_array, cost_indexes, found_cost_indexes

def big_data_organizer_sparda(big_data):

    ''' 
    big_data's first entry  big_data[:][x][0] has a summary information e.g. start-end date of all data and current saldo.

    big_data is in the following format (from second entry to the last entry):

    big_data[:][0] = big_data[0][:][1:-1] = date_array_booking
    big_data[:][1] = big_data[1][:][1:-1] = date_array_transaction
    big_data[:][2] = big_data[2][:][1:-1] = info_array
    big_data[:][3] = big_data[3][:][1:-1] = amount_array_f
    '''
    # Post-process big_data

    # First row of big_data, i.e. big_data[:][x][0] holds a summary information. Get them.
    # get the overall time window of the transactions
    transaction_time_window_overall_s = big_data[:][0][0] , big_data[:][1][0]
    # the current saldo, when this data was subtracted
    current_saldo_f                   = big_data[:][3][0] # also = big_data[:][4][0]

    # From second row until the end, i.e. big_data[:][x][1:-1] all necessary data is stored. Get them.
    # dates when money was really taken/given
    date_array_booking_s = big_data[:][0][1:-1]
    # dates when transaction was initiated
    date_array_transaction_s = big_data[:][1][1:-1]
    # all information available regarding the transaction (e.g. shop name, etc)
    info_array_s   = big_data[:][2][1:-1]
    # amount of the transaction
    amount_array_f = big_data[:][3][1:-1]

    # compute saldo of all transactions for this data (and hence time window)
    saldo_array_f = []
    saldo = 0.0
    for amount in amount_array_f:
        saldo = saldo + amount
        saldo_array_f.append(saldo)
    # Notice that the saldo until the time this data was subtracted can be estimated as:
    # prev_saldo_f = current_saldo_f - saldo_array_f[-1]

    return transaction_time_window_overall_s, current_saldo_f, date_array_booking_s, date_array_transaction_s, info_array_s, amount_array_f, saldo_array_f

def write_to_file_owerwrite(data,filename):
    # write a data to a file. If another file exists with the same name, overwrite it.
    with open (filename, 'w+') as writeFile:
        for info in data:
            writeFile.write(info+"\n")

def write_to_file_add(data,filename):
    # write a data to a file. If another file exists with the same name, add on it.
    with open (filename, 'a') as writeFile:
        for info in data:
            writeFile.write(info+"\n")

def create_data_struct(classifications):
    '''
    per element of the classification, we need:
    - an info array for storing the information of relevant transaction
    - an index array for storing the index of the element in big_data
    - a float for summing up the costs/incomes of the element over big_data

    so, it actually does:

    grocery_array       = []
    grocery_indexes     = []
    insurance_array     = []
    insurance_indexes   = []
    com_int_array       = []
    com_int_indexes     = []
    health_array        = []
    health_indexes      = []
    transport_array     = []
    transport_indexes   = []
    house_array         = []
    house_indexes       = []
    cash_array          = []
    cash_indexes        = []
    sport_array         = []
    sport_indexes       = []
    creditcard_array    = []
    creditcard_indexes  = []
    charity_array       = []
    charity_indexes     = []

    income_array        = []
    income_indexes      = []

    # prepare the sum of individual expenses
    transport_amounts   = 0
    grocery_amounts     = 0
    insurance_amounts   = 0
    com_int_amounts     = 0
    health_amounts      = 0
    house_amounts       = 0
    cash_amounts        = 0
    sport_amounts       = 0
    creditcard_amounts  = 0
    charity_amounts     = 0

    income_amouts = 0 # which is not used, because we already have saldo!
    '''
    for element in classifications:
        #exec ("%s = %f" % (element+'_array',1.0))
        vars()[element+'_array']=[]
        vars()[element+'_indexes']=[]
        vars()[element+'_amounts']=0.0
    # FIXME: how can I return all the created variables automatically? Making them global? 
    #        how can I make them global while using vars() ?