import sys
from random import shuffle
import glob
import os

import numpy as np
import librosa
from tqdm import tqdm
import concurrent.futures
from matplotlib.pyplot import specgram
from keras.utils import to_categorical
from sklearn.preprocessing import LabelEncoder

PARENT_DIR = "data/accents/data/2-processed-wav"
TR_SUB_DIR = [
    "american1",
    "chinese1",
    "korean",
    "japanese",
    "british",
    "french",
    "german",
    "thai",
]
# TR_SUB_DIR = ['singaporean', 'southafrican']
# TS_SUB_DIR = ["indian1"]


class DataLoader:
    def __init__(self):
        self.hey = 1
        self.max_examples_per_class = 100
        self.num_features = 50

    # def extract_feature_threaded(self, file_name):
    # with concurrent.futures.ProcessPoolExecutor(4) as executor:

    def parse_audio_files(self, parent_dir, sub_dirs, file_ext="*.wav"):
        features, labels = np.empty((0, self.num_features)), np.empty(0)
        for _, sub_dir in enumerate(sub_dirs):

            print(sub_dir)
            # files = glob.glob(os.path.join(parent_dir, sub_dir, file_ext))

            # with concurrent.futures.ProcessPoolExecutor(2) as executor:

            #     for out in executor.map(extract_feature, files):
            #         out1, out2 = out
            #         print(out)
            # ext_features = np.hstack([chroma])
            # features = np.vstack([features, ext_features])
            # labels = np.append(labels, label)

            filenames = glob.glob(os.path.join(parent_dir, sub_dir, file_ext))
            if len(filenames) >= self.max_examples_per_class:
                shuffle(filenames)
                filenames = filenames[: self.max_examples_per_class]

            for filename in tqdm(filenames):
                try:
                    mfccs = extract_feature(filename)
                    # mfccs, chroma, mel, contrast, tonnetz = extract_feature(filename)
                except Exception as e:
                    print("Error encountered while parsing file: ", filename)
                    continue
                ext_features = np.hstack([mfccs])
                # ext_features = np.hstack([mfccs, chroma, mel, contrast, tonnetz])
                features = np.vstack([features, ext_features])
                # labels = np.append(labels, filename.split('/')[2].split('-')[1])
                labels = np.append(labels, sub_dir)

        label_encoder = LabelEncoder()
        integer_encoded = label_encoder.fit_transform(labels)
        labels_one_hot = to_categorical(integer_encoded)

        return np.array(features), np.array(labels_one_hot, dtype=np.int)

    def load_data(self):
        # tr_features, tr_labels = self.parse_audio_files(PARENT_DIR,TR_SUB_DIR)
        # ts_features, ts_labels = self.parse_audio_files(PARENT_DIR,TS_SUB_DIR)

        # tr_labels, ts_labels = one_hot_encode(tr_labels, ts_labels)

        # return tr_features, tr_labels, ts_features, ts_labels

        features, labels = self.parse_audio_files(PARENT_DIR, TR_SUB_DIR)

        return features, labels
        # sample_size = len(features)
        # train_size = math.ceil(sample_size * .8)

        # return features[:train_size], labels[:train_size], features[train_size:], labels[train_size:]

    def load_one_sample(self):
        features, labels = np.empty((0, self.num_features)), np.empty(0)
        shuffle(TR_SUB_DIR)
        sub_dir = TR_SUB_DIR[0]

        print(sub_dir)

        filenames = glob.glob(os.path.join(PARENT_DIR, sub_dir, "*.wav"))
        shuffle(filenames)
        filename = filenames[0]

        print(filename)

        try:
            mfccs = extract_feature(filename)
            # mfccs, chroma, mel, contrast, tonnetz = extract_feature(filename)
        except Exception as e:
            print("Error encountered while parsing file: {}".format(filename))
            print("Exiting")
            sys.exit(1)
        ext_features = np.hstack([mfccs])
        # ext_features = np.hstack([mfccs, chroma, mel, contrast, tonnetz])
        features = np.vstack([features, ext_features])
        # labels = np.append(labels, filename.split('/')[2].split('-')[1])
        labels = np.append(labels, sub_dir)

        label_encoder = LabelEncoder()
        integer_encoded = label_encoder.fit_transform(labels)
        labels_one_hot = to_categorical(integer_encoded)

        return np.array(features), np.array(labels_one_hot, dtype=np.int)


def print_name(file_name):
    return file_name, "hey"


def extract_feature(file_name):
    X, sample_rate = librosa.load(file_name)

    # length = (X.shape[0] // 10000 ) * 10000
    # X = X[:length]
    # X = np.array(X)
    # X = np.split(X, 10000)

    # print(X.shape)

    # stft = np.abs(librosa.stft(X))
    mfccs = np.mean(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=50).T, axis=0)
    # chroma = np.mean(librosa.feature.chroma_stft(S=stft, sr=sample_rate).T, axis=0)
    # mel = np.mean(librosa.feature.melspectrogram(X, sr=sample_rate).T, axis=0)
    # contrast = np.mean(
    #     librosa.feature.spectral_contrast(S=stft, sr=sample_rate).T, axis=0
    # )
    # tonnetz = np.mean(
    #     librosa.feature.tonnetz(y=librosa.effects.harmonic(X), sr=sample_rate).T, axis=0
    # )
    # print(len(mfccs)+len(chroma)+len(mel)+len(contrast)+len(tonnetz))
    return mfccs
    # return mfccs, chroma, mel, contrast, tonnetz


if __name__ == "__main__":
    data_loader = DataLoader()
    data_loader.load_data()
