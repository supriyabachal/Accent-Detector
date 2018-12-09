import os
from tqdm import tqdm

CWD = os.getcwd()
DIRECTORY_RAW = 'data/1-raw-mp3/'
DIRECTORY_PROC = 'data/2-processed-wav/'

for accent in os.listdir(os.path.join(CWD, DIRECTORY_RAW)):
    for i in tqdm(range(len(os.listdir(os.path.join(CWD, DIRECTORY_RAW, accent))))):
        for file in os.listdir(os.path.join(CWD, DIRECTORY_RAW, accent)):
            pass
