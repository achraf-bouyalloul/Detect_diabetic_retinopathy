# -*- coding: utf-8 -*-
"""effcineNET_classe_0_1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1QEh-H_bBh3Zjufm44DEcxYhxTYHagq2_
"""

from google.colab import drive
drive.mount('/content/drive')

!pip install efficientnet

import tensorflow as tf
from efficientnet.tfkeras import EfficientNetB0
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import matplotlib.pyplot as plt

# Paramètres
num_classes = 2
input_shape = (224, 224, 3)
batch_size = 32
epochs = 20

# Chargement du modèle EfficientNetB0 pré-entraîné
base_model = EfficientNetB0(weights='imagenet', include_top=False, input_shape=input_shape)

# Ajout de nouvelles couches de classification
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(1024, activation='relu')(x)
predictions = Dense(num_classes, activation='softmax')(x)
model = Model(inputs=base_model.input, outputs=predictions)

# Compilation du modèle
model.compile(optimizer=Adam(lr=0.001), loss='categorical_crossentropy', metrics=['accuracy'])

# Prétraitement des données et augmentation des données
train_datagen = ImageDataGenerator(
    rescale=1.0/255,
    horizontal_flip=True,
    vertical_flip=True,
    rotation_range=30,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    fill_mode='nearest')


chemin_data="chemin-des-classes" # choisi chemin qui contient les deux classe besoin de trainer

train_generator = train_datagen.flow_from_directory(
    chemin_data,
    target_size=input_shape[:2],
    batch_size=batch_size,
    class_mode='categorical')

# Entraînement du modèle avec affichage des informations
history = model.fit(
    train_generator,
    steps_per_epoch=train_generator.samples // batch_size,
    epochs=epochs,
    verbose=1)  # Utilisez verbose=2 pour moins d'informations

# Visualisation des courbes de performances
plt.figure(figsize=(12, 6))

# Loss
plt.subplot(1, 2, 1)
plt.plot(history.history['loss'], label='train')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()

# Accuracy
plt.subplot(1, 2, 2)
plt.plot(history.history['accuracy'], label='train')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()

plt.tight_layout()
plt.show()

chemin_vers_model_weights="chemin-enregistrer-model-version_weights" # chemin ou tu peut enrgestrer votre model
chemin_vers_model="chemin-enregistrer-model-version_weights" # chemin ou tu peut enrgestrer votre model


# Après l'entraînement
model.save_weights(chemin_vers_model_weights)
# Sauvegarder le modèle entraîné
model.save(chemin_vers_model)



