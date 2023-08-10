# -*- coding: utf-8 -*-
"""test_validation.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1cNESA7BcfnQ3ezMkBeoNIDvDzQPyoIi0
"""

from google.colab import drive
drive.mount('/content/drive')

import os
import matplotlib.pyplot as plt
import numpy as np
from keras.applications import DenseNet121
from keras.models import Model
from keras.layers import Dense, GlobalAveragePooling2D
from keras.optimizers import Adam
from keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import Callback

# Dimensions des images en entrée du modèle DenseNet
input_shape = (224, 224, 3)

# Charger le modèle DenseNet pré-entraîné (sans les couches de classification)
base_model = DenseNet121(weights='imagenet', include_top=False, input_shape=input_shape)

# Ajouter des couches de classification personnalisées
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(512, activation='relu')(x)  # Ajoutez des couches Dense supplémentaires si nécessaire
predictions = Dense(5, activation='softmax')(x)  # 5 classes pour votre cas
# Créer le modèle final à évaluer
model = Model(inputs=base_model.input, outputs=predictions)

# Compiler le modèle
model.compile(optimizer=Adam(lr=0.001), loss='categorical_crossentropy', metrics=['accuracy'])


chemin_model="chemin-model-weights-h5" #chemin ou se trouve le fichier de model enrgistrer


# Charger les poids du modèle sauvegardés
model.load_weights(chemin_model)


chemin_data_test="chemin-data-de-test" # # Définir le chemin vers le dossier contenant les images de test classées par classe


# Définir le chemin vers le dossier contenant les images de test classées par classe
test_data_dir = chemin_data_test

# Utiliser le générateur d'images pour le test avec gestion des erreurs
batch_size = 32
test_datagen = ImageDataGenerator(rescale=1. / 255)

test_generator = test_datagen.flow_from_directory(
    test_data_dir,
    target_size=(input_shape[0], input_shape[1]),
    batch_size=batch_size,
    class_mode='categorical',
    shuffle=False  # Assurez-vous que le générateur n'effectue pas de mélange pour une évaluation précise
)

# Effectuer le test avec evaluate()
test_loss, test_accuracy = model.evaluate(test_generator, steps=len(test_generator))
print(f"Perte du test : {test_loss:.4f} - Précision du test : {test_accuracy:.4f}")

# Callback personnalisé pour visualiser l'entraînement en temps réel
class TrainingVisualizer(Callback):
    def __init__(self):
        self.train_loss_history = []
        self.train_accuracy_history = []

    def on_epoch_end(self, epoch, logs=None):
        self.train_loss_history.append(logs['loss'])
        self.train_accuracy_history.append(logs['accuracy'])

        # Tracer les courbes de perte et d'exactitude
        plt.figure(figsize=(12, 6))
        plt.subplot(1, 2, 1)
        plt.plot(self.train_loss_history)
        plt.xlabel('Époque')
        plt.ylabel('Perte')
        plt.title('Courbe de perte d\'entraînement')

        plt.subplot(1, 2, 2)
        plt.plot(self.train_accuracy_history)
        plt.xlabel('Époque')
        plt.ylabel('Exactitude')
        plt.title('Courbe d\'exactitude d\'entraînement')

        plt.show()

chemin_vers_model="chemin-enregistrer-model-version_weights" # chemin ou tu peut enrgestrer votre model version final

# Sauvegarder le modèle entraîné
model.save(chemin_vers_model)
