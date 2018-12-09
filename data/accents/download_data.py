"""
Download MP3 data from http://accent.gmu.edu/browse_language.php
into the /data/ folder
"""
import os
from urllib.error import HTTPError
import wget
import csv_parser

DIRECTORY = 'data/1-raw-mp3/'

querylist = csv_parser.get_list('query.csv')
for index in range(0, len(querylist)):
    native = querylist[index][0] # url path
    accent = querylist[index][1] # classes
    noOfQueries = int(querylist[index][2])

    if not os.path.isdir(DIRECTORY + accent):
        print(DIRECTORY + accent)
        os.makedirs(DIRECTORY + accent)
    for recording in range(1, noOfQueries + 1):
        file_location = DIRECTORY + accent + "/" + native + str(
            recording) + ".mp3"
        file_url = 'http://accent.gmu.edu/soundtracks/' + native + str(
            recording) + '.mp3'
        # print(file_location)
        # print(file_url)
        if os.path.isfile(file_location):
            print("File " + file_location + " already exists.")
            continue
        try:
            print("Downloading " + file_url)
            wget.download(file_url, file_location)
            print("\n")
        except HTTPError:
            print("URL not found")
