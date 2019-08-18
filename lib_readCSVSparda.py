#!/usr/bin/env python
'''
author: burak yuksel
'''
import csv
from utils import *
def return_CSV_data_sparda(filename):
        '''
        This function is a parser of the csv data subtracted/downloaded from
        Sparda-Bank online banking. It returns big_data, which is in the following form:

        big_data's first entry  big_data[:][x][0] has a summary information e.g. start-end date of all data and current saldo.

        big_data is in the following format (from second entry to the last entry):

        big_data[:][0] = big_data[0][:][1:-1] = date_array_booking
        big_data[:][1] = big_data[1][:][1:-1] = date_array_transaction
        big_data[:][2] = big_data[2][:][1:-1] = info_array
        big_data[:][3] = big_data[3][:][1:-1] = amount_array_f
        '''
        date_array_booking    = []
        date_array_transaction    = []
        info_array      = []
        amount_array    = []
        unit_array      = []
        amount_array_f  = []
        big_data        = []
        # open csv
        with open(filename) as csv_file:
            # delimiter is ";" read rows accordingly
            csv_reader = csv.reader(csv_file, delimiter=';')
            # counter for the lines
            line_count = 0
            row_count  = 0
            # loop rows in the csv file
            for row in csv_reader:
                line_count += 1
                # consider non-empty rows
                if row:
                    #print(row_count)
                    #print(row)
                    row_count +=1
                    # for this example, interesting data started from 7 and ended in 269th row
                    # FIXME: detect where row_count should start and end automatically
                    is_date = detect_date_sparda(row)
                    # if row_count>7 and row_count<269:
                    # consider only te data with date: they have the transaction information
                    if is_date:
                        # in sparda logs, they name amounts e.g. 200,00 instead of 200.00
                        # this is problem when converting from str to float or int
                        # here we make it right
                        # similar to what aa=row[3][-3].replace(',','.') would do
                        amount_formatted = ""
                        amount_formatted_2 = ""
                        for i in row[3]:
                            if i==',':
                                i='.'
                            amount_formatted = amount_formatted + i
                            # in sparda logs, amounts more than 999 are stored as 1.200, instead of 1200
                            # this is a problem when converting from str to float or int
                            # here we make it right
                            # amount formats in sparda are as in the following:
                            # X,YY
                            # -X,YY
                            # XX,YY
                            # -XX,YY
                            # XXX,YY
                            # -XXX,YY
                            # X.XXX,YY
                            # -X.XXX,YY
                            # hence if the length of the amount is greater than 7, afforementioned problem occurs.
                            # We create a new string, by combining the left of "." with the right of ".", without including "."
                            # for those amounts that have length greater than 7.
                            # Notice that the location of this problematic "." is amount[-7] (same for amount_formatted[-7])
                            if len(amount_formatted)>7:
                                amount_formatted_2 = amount_formatted[:-7] + amount_formatted[-6:]
                            else:
                                amount_formatted_2 = amount_formatted
                        # append the needed data to the arrays
                        date_array_booking.append(row[0])
                        date_array_transaction.append(row[1])
                        info_array.append(row[2])
                        amount_array.append(amount_formatted_2)
                        amount_array_f.append(float(amount_formatted_2))
                        unit_array.append(row[4]) 
            big_data = [ date_array_booking, date_array_transaction, info_array, amount_array_f]
        return big_data