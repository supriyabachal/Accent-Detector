"""
Convert .mp3 files to .wav files
"""
import os
from pydub import AudioSegment

CWD = os.getcwd()
DIRECTORY_RAW = 'data/1-raw-mp3/'
DIRECTORY_CONV = 'data/2-converted-wav/'

# need to check if all files are there in respective folders
"""
Convert an mp3 file to wav file
"""
def parse_mp3_file(filename, output):
    sound = AudioSegment.from_mp3(filename)
    sound.export(output, format="wav")
    print('Converted {filename}'.format(filename=filename))

for accent in os.listdir(os.path.join(CWD, DIRECTORY_RAW)):
    if not os.path.isdir(os.path.join(CWD, DIRECTORY_CONV, accent)):
        os.makedirs(DIRECTORY_CONV + accent)
    for file in os.listdir(os.path.join(CWD, DIRECTORY_RAW, accent)):
        file_input  = os.path.join(CWD, DIRECTORY_RAW,  accent, os.path.splitext(file)[0] + ".mp3")
        file_output = os.path.join(CWD, DIRECTORY_CONV, accent, os.path.splitext(file)[0] + ".wav")
        # print(file_input)
        # print(file_output)
        try:
            parse_mp3_file(file_input, file_output)
        except FileNotFoundError:
            print("File not found")
