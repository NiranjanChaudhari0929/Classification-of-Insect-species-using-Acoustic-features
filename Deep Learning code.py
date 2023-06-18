# -*- coding: utf-8 -*-
"""Dl part Informal project.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1qYZkKmTR5PME4SDREPKDvjAlLYG9dMfz

Final Model implemented

Use the following
1. The folder Spectrograms_Ai+form , contains all the spectrograms in format Ai where i is an integer
2. Do not change the files of 6 classes shown in the drive
3. No CSV used here
4. It is needed to convert audio files to spectrograms using standard spectrograms codes
5. Provide the path of the folders properly everytime

       xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx


```
# This is formatted as code
```


DL part only needs the folder with all the spectrograms in it in form Ai

ML need the CSV file with the 4 properties .Matlab used to extract the 4 properties of the spectrograms save on drive .

Converting the audio file to spectrogram  (This is just a standard form, provide input on your own)
"""

import librosa
import librosa.display
import matplotlib.pyplot as plt
from google.colab import drive

# Mount Google Drive
drive.mount('/content/drive')

# Load the audio file
audio_path = '/path/to/audio/file.wav'
audio, sr = librosa.load(audio_path)

# Compute the spectrogram
spectrogram = librosa.feature.melspectrogram(audio, sr=sr)

# Convert to decibel scale
spectrogram_db = librosa.power_to_db(spectrogram, ref=np.max)

# Display the spectrogram
plt.figure(figsize=(1000, 400))
librosa.display.specshow(spectrogram_db, sr=sr, x_axis='time', y_axis='mel')
plt.colorbar(format='%+2.0f dB')
plt.title('Spectrogram')
plt.tight_layout()

# Save the spectrogram to Google Drive
save_path = '/content/drive/MyDrive/Spectrogram.png'
plt.savefig(save_path)

"""Here image can be pre proeceesed according to need.

Deep learning model:
"""

import os
import cv2
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from google.colab import drive
from keras.utils import to_categorical


# Mount Google Drive
drive.mount('/content/drive')

# Set the path to the image directory in your Google Drive
image_dir = '/content/drive/MyDrive/InsectSounds_informal_projects/Spectrograms _Ai_form'

# Rest of the code remains the same...

# Set the number of classes
num_classes = 6

# Placeholder for preprocessing function
def preprocess_image(image):
    # Apply any necessary preprocessing steps to the image
    # Replace this with your own preprocessing code
    return image

# Placeholder for label extraction function
def extract_label(filename):
    # Extract the label from the image filename
    # Replace this with your own label extraction code
    label = filename.split('.')[0]  # Extract label excluding file extension

    label_map = {
        'Stored Grain Insects': 0,
        'Soil Invertebrates': 1,
        'Other Species': 2,
        'Insects in woods': 3,
        'Flies and Mosquitoes': 4,
        'Background Sound': 5
    }
    return label_map.get(label, -1)  # Return -1 for unknown labels


# Placeholder to store the preprocessed images and labels
preprocessed_images = []
labels = []

# Iterate over the image files in the directory
for filename in os.listdir(image_dir):
    if filename.endswith('.png'):
        # Load and preprocess the image
        image_path = os.path.join(image_dir, filename)
        image = cv2.imread(image_path)
        image = preprocess_image(image)

        # Append the preprocessed image to the list
        preprocessed_images.append(image)

        # Extract the label from the image filename and append it to the labels list
        label = extract_label(filename)
        labels.append(label)

################################################################################

import cv2
import numpy as np

# Assuming 'preprocessed_images' is your array of preprocessed images with shape (num_images, height, width, 3)

# Define the desired height and width
desired_height = 1000
desired_width = 400

# Create an empty array to store the resized images
resized_images = []

# Iterate over each image and resize it
for image in preprocessed_images:
    resized_image = cv2.resize(image, (desired_width, desired_height))
    resized_images.append(resized_image)

# Convert the list of resized images to a numpy array
resized_images = np.array(resized_images)

################################################################################

# Convert the lists to NumPy arrays
preprocessed_images = np.array(resized_images)
labels = np.array(labels)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    preprocessed_images, labels, test_size=0.2, random_state=42)

# Convert the labels to categorical format
y_train_categorical = to_categorical(y_train, num_classes)
y_test_categorical = to_categorical(y_test, num_classes)

# Define the architecture of your deep learning model
model = Sequential()
model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(1000, 400, 3)))  # Updated input shape
model.add(MaxPooling2D((2, 2)))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D((2, 2)))
model.add(Flatten())
model.add(Dense(64, activation='relu'))
model.add(Dense(num_classes, activation='softmax'))

# Compile the model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Train the model
model.fit(X_train, y_train_categorical, batch_size=32, epochs=10, validation_data=(X_test, y_test_categorical))

# Evaluate the model on the test set
loss, accuracy = model.evaluate(X_test, y_test_categorical)
print("Test Loss:", loss)
print("Test Accuracy:", accuracy)