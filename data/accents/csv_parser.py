"""
Parse csv accents.csv file
Col 1 is the name to identify in the website.
Col 2 is the classification of language in our directory.
"""
import csv

def get_list(filename):
    """
    Returns the list from a csv file
    """
    arraylist = []
    with open(filename) as csvfile:
        readcsv = csv.reader(csvfile, delimiter=',')
        for row in readcsv:
            # Read as tuple or single value
            if len(row) > 1:
                arraylist.append(row)
            else:
                arraylist.append(row[0])
        csvfile.close()
    return arraylist
