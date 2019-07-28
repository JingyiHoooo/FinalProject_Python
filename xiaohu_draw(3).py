#!/bin/python

import dropbox
import datetime
import schedule
import numpy
import string
import requests

from threading import Timer
import time
import sys

import csv

import math
import random
import matplotlib as mpl
import matplotlib.pyplot as plt
import os

import matplotlib.dates as mdate

from matplotlib.ticker import MultipleLocator
from matplotlib.ticker import FormatStrFormatter

import pytz

def E4(x, y):
    # Dropbox access token
    dbx = dropbox.Dropbox('lY_d3DAmzgAAAAAAAAAAdn7IAKZUPyYJXhaYmllRlCFZwhYgt_m6fNafXq8DcgWK')

    # current time
    timestamp = datetime.datetime.now()
    # time gap
    delta = datetime.timedelta(minutes=1)
    # time where the IBI file has been bulit
    filetime = timestamp - delta

    # Re-formatting: datetime->String
    Str_filetime = filetime.strftime('%Y-%m-%d-%H-%M')

    # For testing only
    # Str_filetime = '2019-06-22-22-25'

    # Set parameters for downloading the file
    # Saving path
    download_path = 'C:\\Users\\Administrator\\Desktop\\xiaohu\\IBIData' + Str_filetime + '.txt'
    # File location in dropbox
    path = '/IBI/IBIData' + Str_filetime + '.txt'

    # try download
    try:
        dbx.files_download_to_file(download_path, path, None)
    except:
        print('IBIData' + Str_filetime + '.txt current is not exsit')
        pass
    else:
        print("Successful Downloading /Apps/E4Link" + path + " from Dropbox, overwriting " + download_path + "...")

        # A file downloaded, reformat the file
        resval = numpy.loadtxt(download_path)

        with open(download_path, 'r') as f:
            sum = 0
            count = 0
            lines = f.readlines()  # read the content
            for line in lines:
                for value in line.split():
                    value = value.strip(string.whitespace)
                    sum += float(value)
                    count += 1

            aveIBI = sum / count
            bpm = int(60 / aveIBI)

            draw(x, y, Str_filetime, bpm)

        # with open('bpm_data.csv', 'a', newline='') as f:
        #     csv_write = csv.writer(f)
        #     csv_write.writerow([Str_filetime, bpm])
        #     f.close()

        print('The average IBI value(s):', aveIBI, '\n' + 'The heart beat rate(bpm):', bpm, '\n')

def bodyE4():

    x = []
    y = []

    plt.ion()
    plt.figure(1)
    plt.tick_params(axis='x', rotation=90)
    plt.title('bpm verus time')
    plt.xlabel('time')
    plt.ylabel('bpm')

    schedule.every(1).minutes.do(E4, x, y)
    while True:
        schedule.run_pending()

def draw(x, y, Str_filetime, bpm):

    print ('start drawing')

    plt.clf()
    x.append(Str_filetime)
    y.append(bpm)
    plt.plot(x, y, '-r')
    plt.pause(0.01)


if __name__ == "__main__":
    bodyE4()
    print ('here')
