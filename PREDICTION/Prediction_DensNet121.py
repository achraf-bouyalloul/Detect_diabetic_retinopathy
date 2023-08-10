# -*- coding: utf-8 -*-
"""Pridection_V_sans_filtre.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ZeM7t6jO6xTIHv_tI0PABJw17oYn2Xq0
"""

from google.colab import drive
drive.mount('/content/drive')

import os
import csv
import numpy as np
from keras.applications import DenseNet121
from keras.models import Model
from keras.layers import Dense, GlobalAveragePooling2D
from keras.optimizers import Adam
from PIL import Image

# Dimensions des images en entrée du modèle DenseNet
input_shape = (224, 224, 3)

# Charger le modèle DenseNet pré-entraîné (sans les couches de classification)
base_model = DenseNet121(weights='imagenet', include_top=False, input_shape=input_shape)

# Ajouter des couches de classification personnalisées
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(512, activation='relu')(x)
predictions = Dense(5, activation='softmax')(x)  # 5 classes pour votre cas

# Créer le modèle final
model = Model(inputs=base_model.input, outputs=predictions)

# Charger les poids du modèle sauvegardés
model.load_weights('/content/drive/MyDrive/model_weightsV2.h5')

# Dossier contenant les images que vous souhaitez prédire
image_path = '/content/drive/MyDrive/data_finalV2/2/000c1434d8d7.png'

image = Image.open(image_path)
image = image.resize((input_shape[0], input_shape[1]))
image_array = np.array(image)
image_array = np.expand_dims(image_array, axis=0)
image_array = image_array.astype('float32')
image_array /= 255.0
predictions = model.predict(image_array)
predicted_class_index = np.argmax(predictions)
print("la classe est :",predicted_class_index)