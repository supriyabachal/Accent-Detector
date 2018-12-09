"""
Downloads data from www.jbistudios.com
"""
import os
# from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import wget
from urllib.request import Request, urlopen

CWD = os.getcwd()
DOWNLOAD_PATH = 'data/raw/'

# The first number of the tuple is the position of the language name in the mp3 url
URL1 = 7,'https://www.jbistudios.com/english-somali-swahili-voice-over-dubbing-samples'
URL2 = 7,'https://www.jbistudios.com/english-mexican-spanish-brazilian-portuguese-voice-over-dubbing-samples'
URL3 = 7,'https://www.jbistudios.com/chinese-japanese-korean-arabic-voice-over-dubbing-samples'
URL4 = 7,'https://www.jbistudios.com/french-english-german-spanish-voice-over-dubbing-samples'
URL5 = 6,'https://www.jbistudios.com/australian-english-hawaiian-samoan-voice-over-dubbing-samples'
URLS = [URL1, URL2, URL3, URL4, URL5]

# Server to download from
HEADER = 'https://cdn2.hubspot.net/hubfs/702211/2_Audio'

def get_sample_voices():

    for url in URLS:
        # Load and save page
        print("\nGetting links from " + url[1])
        page = urlopen(url[1])
        soup = BeautifulSoup(page, 'html.parser')
        audios = soup.findAll('audio')

        for audio in audios:
            file_url_hint = audio['src']
            if url[1] == URL1[1]:
                file_url_hint = 'https:' + file_url_hint

            file_url = ''
            sections = file_url_hint.split("/")
            if sections[5] == 'Most_Requested_Languages': # these languages are in position 5
                language = sections[5+1]
                file_location = os.path.join(CWD,DOWNLOAD_PATH,language,sections[5+2].split("?")[0])
                file_url = os.path.join(HEADER, sections[5], sections[6], sections[5+2].split("?")[0])
            elif url[1] == URL5[1]: # Australia
                language = sections[url[0]]
                file_location = os.path.join(CWD,DOWNLOAD_PATH,language,sections[url[0]+1].split("?")[0])
                file_url = os.path.join(HEADER, sections[url[0]-1], sections[url[0]], sections[url[0]+1].split("?")[0])
            else:
                language = sections[url[0]]
                file_location = os.path.join(CWD,DOWNLOAD_PATH,language,sections[url[0]+1].split("?")[0])
                file_url = os.path.join(HEADER, sections[url[0]-2], sections[url[0]-1], sections[url[0]], sections[url[0]+1].split("?")[0])

            # Create folder if havent
            if not os.path.isdir(os.path.join(CWD,DOWNLOAD_PATH,language)):
                os.makedirs(os.path.join(CWD,DOWNLOAD_PATH,language))

            # If file exists, skip
            if os.path.lexists(file_location):
                continue
                
            try:
                print("Downloading " + file_url)
                download_mp3_file(file_url, file_location)
            except HTTPError:
                print("Cannot download file.")
                try:
                    print("Trying " + file_url_hint)
                    download_mp3_file(file_url_hint, file_location)
                except HTTPError:
                    print("Cannot download file (2 tries).")

def download_mp3_file(url, filename):

    # Need to request with header otherwise you get blocked cos you're a bot
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    mp3 = urlopen(req)
    # Open a file for reading
    output = open(filename,'wb')
    # Write file in binary
    output.write(mp3.read())
    # Close file
    output.close()

if __name__ == '__main__':
    get_sample_voices()

    # query = sys.argv[1]
    # find_no_of_results(query)
