import csv
import cv2
import numpy as np

lines = []
with open("./6.19/driving_log.csv") as csvfile:
	reader = csv.reader(csvfile)
	for line in reader:
		lines.append(line)

images = []
measurements = []
for line in lines:
	for i in range(3):
		souce_path = line[i]
		filename = souce_path.split("/")[-1]
		current_path="./6.19/IMG/" + filename
		image = cv2.imread(current_path)
		images.append(image)
		measurement = float(line[3])
		constant = 0.2
		measurements.append(measurement)
		measurements.append(measurement + constant)
		measurements.append(measurement - constant)

X_train = np.array(images)
y_train = np.array(measurements)

print(X_train[16])
print(y_train[16])


augmented_images, augmented_measurements = [],[]
for image, measurement in zip(images, measurements):
	augmented_images.append(image)
	augmented_measurements.append(measurement)
	augmented_images.append(cv2.flip(image,1))
	augmented_measurements.append(measurement * (-1))

X_train = np.array(augmented_images)
y_train = np.array(augmented_measurements)

# model

from keras.models import Sequential
from keras.layers import Flatten, Dense, Lambda, Cropping2D, Convolution2D

model = Sequential()
model.add(Lambda(lambda x: x/255.0 - .5, input_shape=(160,320,3)))
model.add(Cropping2D(cropping=((70,25), (0,0))))
model.add(Convolution2D(24,5,5, subsample=(2,2), activation= "relu"))
model.add(Convolution2D(36,5,5, subsample=(2,2), activation= "relu"))
model.add(Convolution2D(48,5,5, subsample=(2,2), activation= "relu"))
model.add(Convolution2D(64,3,3,  activation= "relu"))
model.add(Convolution2D(64,3,3,  activation= "relu"))

model.add(Flatten())
model.add(Dense(100))
model.add(Dense(50))
model.add(Dense(10))
model.add(Dense(1))

model.compile(loss='mse', optimizer='adam')
history_object = model.fit(X_train,y_train, validation_split=0.2, shuffle= True, nb_epoch=5)

model.save('model.h5')

### print the keys contained in the history object
import matplotlib.pyplot as plt

print(history_object.history.keys())

### plot the training and validation loss for each epoch
plt.plot(history_object.history['loss'])
plt.plot(history_object.history['val_loss'])
plt.title('model mean squared error loss')
plt.ylabel('mean squared error loss')
plt.xlabel('epoch')
plt.legend(['training set', 'validation set'], loc='upper right')
plt.show()



import gc
gc.collect()

