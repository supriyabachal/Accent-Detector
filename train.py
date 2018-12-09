import matplotlib.pyplot as plt
from keras.models import Sequential, Model
from keras.layers import Dense, Input, BatchNormalization
import numpy as np

from data_loader import DataLoader

# Load data
data_loader = DataLoader()
x, y = data_loader.load_data()

input_dim = len(x[0])
output_dim = len(y[0])

# print(X_train[0].shape)

# # Model
# model = Sequential()
# model.add()      # shape of output of X
# model.add(Dense(units=512))
# model.add(Dense(units=1024))
# model.add(Dense(units=100))
# model.add(Dense(units=10, activation='softmax'))

# # Model
# model = Sequential([
#     Dense(256, input_dim=193),
#     Dense(256, input_dim=193),
#     Dense(256, input_dim=193),
#     Dense(256, input_dim=193),
# ])



# Model
layers = [256, 1024, 2048, 5096, 400, 100]
inputs = Input(shape=(input_dim,))

for units in layers:
    layer = Dense(units, activation="relu")(inputs)
    layer = BatchNormalization(momentum=0.8)(layer)

outputs = Dense(output_dim, activation="softmax")(layer)
model = Model(inputs=inputs, outputs=outputs)
model.compile(loss="categorical_crossentropy", optimizer="sgd", metrics=["accuracy"])
history = model.fit(
    x=x,
    y=y,
    batch_size=5,
    epochs=100,
    shuffle=True,
    validation_split=0.8,
    #   validation_data=(X_test, Y_test),
    verbose=1,
)




model.save("mymodel.h5")

# Plot training & validation accuracy values
plt.plot(history.history['acc'])
plt.plot(history.history['val_acc'])
plt.title('Model accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Train', 'Test'], loc='upper left')
plt.show()

# Plot training & validation loss values
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Model loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['Train', 'Test'], loc='upper left')
plt.show()

# print(model.predict(np.array([[1,2,3,4,5,6,7,8,9,20,11,2],])))

# class AccentDetector():
#     def __init__(self):
#         self.hey = 1
#         self.model = self.train()
#         self.model.compile()

#     def model(self):
#         model = Sequential()
#         model.add(Dense(1, input_dim=8))
#         model.add(Activation('relu'))

#         return Model()

#     def train(self):
#         self.model.fit()


# if __name__ == "__main__":
#     accent_detector = AccentDetector()
#     accent_detector.train()
