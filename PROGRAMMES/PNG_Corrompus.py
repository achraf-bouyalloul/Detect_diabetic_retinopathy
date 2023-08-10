# -*- coding: utf-8 -*-
"""png_corrompus.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1cICjTn6CboFHluDqPHVsXUgPYJzE1saq
"""

!pip install opencv-python

from google.colab import drive
drive.mount('/content/drive')

import os
from PIL import Image

import os
from PIL import Image

def is_png(file_path):
    # Vérifier si le fichier a l'extension .png
    return file_path.lower().endswith('.png')

def is_corrupted_png(file_path):
    try:
        # Essayer de charger l'image pour vérifier si elle est corrompue
        with Image.open(file_path) as img:
            img.verify()
        return False
    except (IOError, SyntaxError):
        return True

def delete_corrupted_png_in_folder(folder_path):
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if is_png(file_path) and is_corrupted_png(file_path):
            # Supprimer le fichier corrompu
            os.remove(file_path)
            print(f"Le fichier corrompu '{file_name}' a été supprimé.")

def delete_corrupted_png_in_all_folders(root_directory):
    # Parcourir les cinq dossiers "0", "1", "2", "3", "4"
    for subfolder in ["0", "1", "2", "3", "4"]:
        subfolder_path = os.path.join(root_directory, subfolder)
        if os.path.isdir(subfolder_path):
            print(f"Traitement du dossier '{subfolder}'...")
            delete_corrupted_png_in_folder(subfolder_path)

# Exemple d'utilisation :
if __name__ == "__main__":
    root_directory_path = "/content/drive/MyDrive/class 2015"
    delete_corrupted_png_in_all_folders(root_directory_path)