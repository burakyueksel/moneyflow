#!/usr/bin/env python
'''
author: burak yuksel
'''
from lib_plot import *
from fpdf import FPDF
from PIL import Image
import os

def plotter(all_costs, all_incomes, grocery_amounts, insurance_amounts, com_int_amounts, health_amounts, transport_amounts, house_amounts, cash_amounts, sport_amounts, creditcard_amounts, charity_amounts, total_notfound_cost_amounts, transaction_time_window_overall_s):
    # Data to plot
    labels = 'Grocery', 'Insurance', 'COM', 'Health', 'Transport', 'House', 'Cash', 'Sport', 'CreditCard', 'Charity', 'Others'
    sizes = [grocery_amounts/all_costs*100, insurance_amounts/all_costs*100, com_int_amounts/all_costs*100, health_amounts/all_costs*100, \
            transport_amounts/all_costs*100, house_amounts/all_costs*100, cash_amounts/all_costs*100, sport_amounts/all_costs*100, \
            creditcard_amounts/all_costs*100, charity_amounts/all_costs*100, total_notfound_cost_amounts/all_costs*100]
    colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue', 'gold', 'yellowgreen', 'lightcoral', 'lightskyblue', 'gold', 'yellowgreen', 'lightcoral']
    explode = (0, 0, 0, 0, 0.1, 0, 0, 0, 0, 0, 0.1)  # explode 1st slice
    title = 'Cost Distribution between {} and {}'.format(transaction_time_window_overall_s[0],transaction_time_window_overall_s[1])
    # Plot
    plot_pie(sizes, explode, labels, colors, title)

    x = 'Grocery', 'Insurance', 'COM', 'Health', 'Transport', 'House', 'Cash', 'Sport', 'CreditCard', 'Charity', 'Others'
    y = [grocery_amounts, insurance_amounts, com_int_amounts, health_amounts, transport_amounts, house_amounts, cash_amounts, sport_amounts, creditcard_amounts, charity_amounts, total_notfound_cost_amounts]
    title = 'Costs between {} and {}'.format(transaction_time_window_overall_s[0],transaction_time_window_overall_s[1])
    plot_bar(x,y,1/1.5,title)

    x = 'All incomes' , 'All costs'
    y = [all_incomes, all_costs]
    title = 'Incomes vs Costs between {} and {}'.format(transaction_time_window_overall_s[0],transaction_time_window_overall_s[1])
    plot_bar(x,y,1/1.5,title)

    labels = 'Spent', 'Saved'
    sizes  = [-all_costs/all_incomes*100, 100-(-all_costs/all_incomes*100)]
    colors = ['red','gold']
    explode = (0.1, 0)
    title = 'Spent vs Saved % of all income between {} and {}'.format(transaction_time_window_overall_s[0],transaction_time_window_overall_s[1])
    plot_pie(sizes, explode, labels, colors, title)

def printer(all_costs,all_incomes,current_saldo_f,saldo_array_f,transaction_time_window_overall_s):

    msg1    = "total cost is: {} EUR".format(all_costs)
    print(msg1)
    msg2    = "total income is: {} EUR".format(all_incomes)
    print(msg2)
    msg3    = "costs are {} % of the incomes. This means {} % of the incomes are saved.".format((-all_costs/all_incomes*100), 100-(-all_costs/all_incomes*100))
    print(msg3)
    msg4    = "Between {} and {}, saldo is increased (+) or decreased (-) with {} EUR".format( transaction_time_window_overall_s[0], transaction_time_window_overall_s[1], saldo_array_f[-1]) 
    print(msg4)
    msg5    = "Estimated previous saldo on {} was {} EUR".format(transaction_time_window_overall_s[0], (current_saldo_f - saldo_array_f[-1]))
    print(msg5)
    #msg = "transport is {} % of the all costs.".format(transport_amounts/all_costs*100)
    #print(msg)
    messages = [msg1, msg2, msg3, msg4, msg5]
    return messages

def reporter(path_to_plots,path_to_pdf,messages):
    image_list = []
    for filename in os.listdir(path_to_plots):
        if filename.endswith(".png"):
            image_list.append("plots/" + filename)
        else:
            continue
    pdf = FPDF()
    for image in image_list:
        pdf.add_page()
        pdf.image(image, x=10, y=10, w=140, h=100)
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    for i in range(len(messages)):
        pdf.cell(40,200+i*10,messages[i])
    pdf.output(path_to_pdf, "F")