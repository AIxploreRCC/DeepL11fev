# -*- coding: utf-8 -*-
"""Flower-Classification-Web-App-Streamlit

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/19InVbbNxa4uuK1ec67xq_6H85V-4cduf
"""

import matplotlib.pyplot as plt
import numpy as np
import os
import PIL
import tensorflow as tf

from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential

from google.colab import drive
drive.mount('/content/drive')

import pathlib
dataset_url = 'https://storage.googleapis.com/download.tensorflow.org/example_images/flower_photos.tgz'
data_dir = tf.keras.utils.get_file('flower_photos', origin=dataset_url, untar=True)
data_dir = pathlib.Path(data_dir)

roses = list(data_dir.glob('roses/*'))
print(roses[0])
PIL.Image.open(str(roses[0]))

img_height,img_width=180,180
batch_size=32
train_ds = tf.keras.preprocessing.image_dataset_from_directory(
  data_dir,
  validation_split=0.2,
  subset="training",
  seed=123,
  image_size=(img_height, img_width),
  batch_size=batch_size)

val_ds = tf.keras.preprocessing.image_dataset_from_directory(
  data_dir,
  validation_split=0.2,
  subset="validation",
  seed=123,
  image_size=(img_height, img_width),
  batch_size=batch_size)

class_names = train_ds.class_names
print(class_names)

import matplotlib.pyplot as plt

plt.figure(figsize=(10, 10))
for images, labels in train_ds.take(1):
  for i in range(9):
    ax = plt.subplot(3, 3, i + 1)
    plt.imshow(images[i].numpy().astype("uint8"))
    plt.title(class_names[labels[i]])
    plt.axis("off")

num_classes = 5

model = Sequential([
  layers.experimental.preprocessing.Rescaling(1./255, input_shape=(img_height, img_width, 3)),
  layers.Conv2D(16, 3, padding='same', activation='relu'),
  layers.MaxPooling2D(),
  layers.Conv2D(32, 3, padding='same', activation='relu'),
  layers.MaxPooling2D(),
  layers.Conv2D(64, 3, padding='same', activation='relu'),
  layers.MaxPooling2D(),
  layers.Flatten(),
  layers.Dense(128, activation='relu'),
  layers.Dense(num_classes,activation='softmax')
])

model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

epochs=10
history = model.fit(
  train_ds,
  validation_data=val_ds,
  epochs=epochs
)

tf.keras.models.save_model(model,'my_model2.hdf5')



# Commented out IPython magic to ensure Python compatibility.
# %%writefile app.py
# import streamlit as st
# import tensorflow as tf
# import streamlit as st
# 
# 
# @st.cache(allow_output_mutation=True)
# def load_model():
#   model=tf.keras.models.load_model('/content/my_model2.hdf5')
#   return model
# with st.spinner('Model is being loaded..'):
#   model=load_model()
# 
# st.write("""
#          # Flower Classification
#          """
#          )
# 
# file = st.file_uploader("Please upload an brain scan file", type=["jpg", "png"])
# import cv2
# from PIL import Image, ImageOps
# import numpy as np
# st.set_option('deprecation.showfileUploaderEncoding', False)
# def import_and_predict(image_data, model):
#     
#         size = (180,180)    
#         image = ImageOps.fit(image_data, size, Image.ANTIALIAS)
#         image = np.asarray(image)
#         img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#         #img_resize = (cv2.resize(img, dsize=(75, 75),    interpolation=cv2.INTER_CUBIC))/255.
#         
#         img_reshape = img[np.newaxis,...]
#     
#         prediction = model.predict(img_reshape)
#         
#         return prediction
# if file is None:
#     st.text("Please upload an image file")
# else:
#     image = Image.open(file)
#     st.image(image, use_column_width=True)
#     predictions = import_and_predict(image, model)
#     score = tf.nn.softmax(predictions[0])
#     st.write(prediction)
#     st.write(score)
#     print(
#     "This image most likely belongs to {} with a {:.2f} percent confidence."
#     .format(class_names[np.argmax(score)], 100 * np.max(score))
# )

