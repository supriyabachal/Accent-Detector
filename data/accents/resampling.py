"""
1. Convert from MP3 to WAV
2. Resample WAV file
"""
import os
import math
import sys
import ffmpy
from tqdm import tqdm
from pydub import AudioSegment
from pydub.utils import make_chunks

# Suppress tqdm warnings
tqdm.monitor_interval = 0

CWD = os.getcwd()
DIRECTORY_RAW = 'data/1-raw-mp3/'
DIRECTORY_PROC = 'data/2-processed-wav/'

cropped = 10 * 1000
RATE = 44100 #16000
AVG_DURATION = 20
AVG_VOLUME = -23.5

# need to check if all files are there in respective folders

def parse_mp3_file():
    """
    Resample the MP3 files in the data directory to WAV files with sample rate 16,000 Hz
    """

    cannotresample = []
    total_duration = 0
    total_dB = 0
    total_samples = 0

    for accent in os.listdir(os.path.join(CWD, DIRECTORY_RAW)):

        if accent == ".DS_Store":
            continue

        print(" " + accent)
        if not os.path.isdir(os.path.join(CWD, DIRECTORY_PROC, accent)):
            os.makedirs(DIRECTORY_PROC + accent)

        for file in tqdm(os.listdir(os.path.join(CWD, DIRECTORY_RAW, accent))):

            # Debugging
            # if file != "english70.mp3":
                # continue

            if file == ".DS_Store":
                continue
                
            # Set name of MP3 to read from and export pathname
            file_input  = os.path.join(CWD, DIRECTORY_RAW,  accent, os.path.splitext(file)[0] + ".mp3")
            file_output1 = os.path.join(CWD, DIRECTORY_PROC, accent, os.path.splitext(file)[0] + "_tmp.wav")
            file_output2 = os.path.join(CWD, DIRECTORY_PROC, accent, os.path.splitext(file)[0] + ".wav")

            # Debugging
            # print(file_input)

            # Get average duration
            # audiowav = AudioSegment.from_file(file_input)
            # total_duration += audiowav.duration_seconds
            # total_samples += 1
            # print(total_duration/total_samples)

            # Get average dB
            # audiowav = AudioSegment.from_file(file_input)
            # total_dB += audiowav.dBFS
            # total_samples += 1
            # print(total_dB/total_samples)



            try:
                
                # Read audio
                audiowav = AudioSegment.from_file(file_input)
                
                # TODO sounds muffled!!!
                # Resample the rate
                # audiowav = audiowav.set_frame_rate(RATE)
                
                # Crop audio
                audio = audiowav[:cropped]

                # Normalise volume
                change_in_dbfs = AVG_VOLUME - audiowav.dBFS
                audiowav = audiowav.apply_gain(change_in_dbfs)

                # Normalise speed
                speed_multiplier = 1 + (audiowav.duration_seconds - AVG_DURATION) / AVG_DURATION
                # print(speed_multiplier)

                
                
                # if abs(1-speed_multiplier) > 0.3:
                    # flag = True
                # audiowav = speed_change(audiowav, speed=speed_multiplier)


                


                # Normalise pitch
                # speed = 2.0 ^ octaves
                # octaves = log(speed)/log(2.0)
                # shift the pitch up by half an octave (speed will increase proportionally)
                # octaves = math.log(1/speed_multiplier)/math.log(2.0)
                # print(audiowav.frame_rate)
                # new_sample_rate = int(audiowav.frame_rate * (2.0 ** octaves))
                # print(new_sample_rate)
                # keep the same samples but tell the computer they ought to be played at the 
                # new, higher sample rate. This file sounds like a chipmunk but has a weird sample rate.
                # audiowav = audiowav._spawn(audiowav.raw_data, overrides={'frame_rate': new_sample_rate})
                # now we just convert it to a common sample rate (44.1k - standard audio CD) to 
                # make sure it works in regular audio players. Other than potentially losing audio quality (if
                # you set it too low - 44.1k is plenty) this should now noticeable change how the audio sounds.
                audiowav = audiowav.set_frame_rate(RATE)

                

                # Export wav file
                audiowav.export(out_f=file_output1, format='wav')

                # Debugging
                # audiowav.export(file_output1, format="wav")

                ffmpy.FFmpeg(
                    inputs={file_output1: None}, 
                    outputs={file_output2: ["-filter:a", "atempo=" + str(speed_multiplier)]},
                    global_options=['-v 0']
                    ).run()

                os.remove(file_output1)

            except Exception:
                cannotresample.append(file_output2)

    # Show files that were not resampled
    if not cannotresample:
        print("Could not resample:")
        for file in cannotresample:
            print(file)

def speed_change(audio, speed):
    """
    Manually override the frame_rate. This tells the computer how many
    samples to play per second
    """
    sound_with_altered_frame_rate = audio._spawn(audio.raw_data, overrides={
        "frame_rate": int(audio.frame_rate * speed)
    })

    # convert the sound with altered frame rate to a standard frame rate
    # so that regular playback programs will work right. They often only
    # know how to play audio at standard frame rate (like 44.1k)
    return sound_with_altered_frame_rate.set_frame_rate(audio.frame_rate)


def resample(file):
    """ 
    Parse a single mp3 file
    """
    output = "/Users/raimibinkarim/Desktop/inference.wav"
    try:
        audiowav = AudioSegment.from_file(file).set_frame_rate(RATE)
        audio = audiowav[:cropped]
        audio.export(out_f=output, format='wav')
    except Exception:
        print("error")

def create_chunk(file):
    """
    Create chunks of a certain length for a file
    """
    sound = AudioSegment.from_file(file , "mp3") 
    chunk_length_ms = 3000 # pydub calculates in millisec
    chunks = make_chunks(sound, chunk_length_ms) #Make chunks of one sec

    #Export all of the individual chunks as wav files
    for i, chunk in enumerate(chunks):
        chunk_name = "chunk{0}.wav".format(i)
        print("exporting", chunk_name)
        chunk.export(chunk_name, format="wav")

if __name__ == "__main__":
    parse_mp3_file()
    # filename = sys.argv[1]
    # if filename == "":
        # parse_mp3_file()
    # else:
        # create_chunk(filename)
