"""
Rearrange downloaded recordings to folders
according to country origin (english)
"""
import os
from urllib.error import HTTPError
import wget
import csv_parser

CWD = os.getcwd()
DIRECTORY = 'data/1-raw-mp3/'
METADIRECTORY = 'metadata/'

# Get all accents from data/metadata/ folder
accents = []
for file in os.listdir(os.path.join(CWD, 'data', METADIRECTORY, 'english')):
    accents.append(file.split(".")[0])

for accent in accents:
    print(accent)
    accentList = csv_parser.get_list('data/metadata/english/' + accent + '.csv')
    for file in accentList:

        if not os.path.isdir(os.path.join(CWD, DIRECTORY + accent)):
            os.makedirs(DIRECTORY + accent)

        # rename from old folder to new folde
        old_file = os.path.join(CWD, DIRECTORY + 'native', file + '.mp3')
        new_file = os.path.join(CWD, DIRECTORY + accent, file + '.mp3')

        # If exist, move/rename. Else, download
        if os.path.isfile(old_file):
            print("Renaming " + old_file)
            os.rename(old_file, new_file)
        elif os.path.isfile(new_file):
            print("File " + old_file + " already exists.")
        else:
            try:
                file_url = 'http://accent.gmu.edu/soundtracks/' + file + '.mp3'
                print("Downloading from " + file_url + "\n")
                wget.download(file_url, new_file)
            except HTTPError:
                print("Cannot download " + file_url)


