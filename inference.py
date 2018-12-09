import numpy as np
from keras.models import load_model

from data_loader import DataLoader

data_loader = DataLoader()
x, y = data_loader.load_one_sample()

model = load_model('mymodel.h5')

print(model.predict(x))
print(model.layers[1].output)
print(y)