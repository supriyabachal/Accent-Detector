"""
Returns no of available recordings
"""
import sys
from urllib.request import urlopen
from bs4 import BeautifulSoup

def find_no_of_results(language):
    """
    Get no. of recordings for a specified language
    """

    URL = 'http://accent.gmu.edu/browse_language.php?function=find&language='+ language

    # Load and save page
    page = urlopen(URL)
    soup = BeautifulSoup(page, 'html.parser')
    name_box = soup.find('h5').text.strip()
    print(name_box)

    # Split result into an array and get the integer of no. of results
    words = name_box.split(" ")
    try:
        ind = words.index("result(s)")
        print(words[ind-1])
        return(words[ind-1])
    except IndexError:
        print("Cannot find.")
        return -1

def get_sample_voices():

    URL = 'https://www.jbistudios.com/english-somali-swahili-voice-over-dubbing-samples'
    # Load and save page
    page = urlopen(URL)
    soup = BeautifulSoup(page, 'html.parser')
    name_box = soup.findAll('audio')
    print(name_box[0]['src'])

    # Split result into an array and get the integer of no. of results
    # words = name_box.split(" ")
    # try:
    #     ind = words.index("result(s)")
    #     print(words[ind-1])
    #     return(words[ind-1])
    # except IndexError:
    #     print("Cannot find.")
    #     return -1

if __name__ == '__main__':
    # get_sample_voices()

    query = sys.argv[1]
    find_no_of_results(query)
