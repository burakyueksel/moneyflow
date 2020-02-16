#!/usr/bin/env python
'''
author: burak yuksel
'''

import matplotlib.pyplot as plt

def plot_plain(data,xlabel,ylabel):

    fig = plt.figure()
    plt.plot(data)
    plt.xlabel (xlabel)
    plt.ylabel (ylabel)
    plt.grid()
    figpath="plots/plain.png"
    fig.savefig(figpath)
    #plt.show()

    return plt

def plot_plain2(xdata, ydata, xlabel, ylabel):

    fig, ax = plt.figure()
    plt.plot(xdata,ydata)
    plt.xlabel (xlabel)
    plt.ylabel (ylabel)
    '''
    for label in ax.xaxis.get_ticklabels()[::2]:
        label.set_visible(False)
    '''
    n = 7  # Keeps every 7th label
    [l.set_visible(False) for (i,l) in enumerate(ax.xaxis.get_ticklabels()) if i % n != 0]
    plt.grid()
    figpath="plots/plain2.png"
    fig.savefig(figpath)
    #plt.show()

    return plt

def plot_pie(sizes, explode, labels, colors, title):
    
    fig = plt.figure()
    plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
    plt.title(title)
    plt.axis('equal')
    figpath="plots/"+title+".png"
    fig.savefig(figpath)
    #plt.show()

    return plt

def plot_bar(x,y,width,title):

    fig = plt.figure()
    plt.xticks(rotation=45)
    plt.bar(x,y,width,color="blue")
    plt.title(title)
    figpath="plots/"+title+".png"
    fig.savefig(figpath)
    #plt.show()

    return plt