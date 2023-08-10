# -*- coding: utf-8 -*-
"""effcientnetB5_filtre.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1jPgzSdNsjOuAdtGdBSZAxBNuvtG7KQ6e
"""

from google.colab import drive
drive.mount('/content/drive')

!pip install tensorflow

import tensorflow as tf
from tensorflow.keras.applications import EfficientNetB5
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import ModelCheckpoint, CSVLogger



chemin_data="chemin-de-dossier" #chemin de dossier contient les cinq dossiers se classe 0 1 2 3 4  (tu peut chosi avec filtre ou non )

# Répertoire contenant vos données d'entraînement
train_data_dir = chemin_data

# Nombre de classes dans votre ensemble de données
num_classes = 5

# Dimensions des images en entrée
input_shape = (224, 224)

# Créer le modèle EfficientNetB5 pré-entraîné sans la couche de classification finale
base_model = EfficientNetB5(weights='imagenet', include_top=False, input_shape=(224, 224, 3))

# Ajouter une nouvelle couche de classification adaptée à votre tâche
x = GlobalAveragePooling2D()(base_model.output)
output = Dense(num_classes, activation='softmax')(x)

# Créer le modèle final
model = Model(inputs=base_model.input, outputs=output)

# Compiler le modèle
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Augmentation de données pour améliorer la généralisation du modèle
train_datagen = ImageDataGenerator(
    rescale=1./255,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True
)

# Chargez les images depuis le répertoire, les redimensionner à input_shape et les préparer pour l'entraînement
train_generator = train_datagen.flow_from_directory(
    train_data_dir,
    target_size=input_shape,
    batch_size=32,
    class_mode='categorical'
)




# Définir le nombre d'étapes par époque en fonction du nombre total d'images d'entraînement et de la taille du lot
steps_per_epoch = train_generator.n // train_generator.batch_size


# Entraîner le modèle sur l'ensemble de données d'entraînement en utilisant fit
num_epochs = 15
for epoch in range(num_epochs):
    print(f"Epoch {epoch+1}/{num_epochs}")

    model.fit(
        train_generator,
        steps_per_epoch=steps_per_epoch,
        epochs=1,
        callbacks=[model_checkpoint, csv_logger]
    )
    print("ici",epoch+1)
    print("\n")



chemin_vers_model_weights="chemin-enregistrer-model-version_weights" # chemin ou tu peut enrgestrer votre model
chemin_vers_model="chemin-enregistrer-model-version_weights" # chemin ou tu peut enrgestrer votre model

# Après l'entraînement
model.save_weights(chemin_vers_model_weights)

# Sauvegarder uniquement les poids du modèle
model.save_weights(chemin_vers_model)