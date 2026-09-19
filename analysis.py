import os
import csv
import numpy as np
from PIL import Image

IMAGE_DIR = "./images_720p" # Dossier d'images à analyser (images, images_720p ou images_480p)
OUTPUT_DIR = "./data" # Dossier de sortie pour le csv

def main():
    # Definition de la structure du csv avec les légendes
    data = [["name","width","height","aspectRatio","meanHue","meanSaturation","meanValue", "medianHue", "medianSaturation", "medianValue"]]
    files = os.listdir(IMAGE_DIR) # On récupère les images du dossier choisi, doit se situer au même endroit que le fichier main.py
    for index, name in enumerate(files): # Pour chaque fichier
        try:
            image = Image.open(f"{IMAGE_DIR}/{name}").convert("HSV") # On ouvre l'image en format HSV
            print(f"Parsing data from image : {name}")
            
            # On crée une nouvelle ligne contenant le nom et on lui rajoute les données dans l'ordre
            row = [name] # Nom
            row.append(image.width) # Largeur
            row.append(image.height) # Hauteur
            row.append(image.width / image.height) # Aspect ratio
            hsv_array = np.array(image)
            hue, saturation, value = hsv_array[:, :, 0], hsv_array[:, :, 1], hsv_array[:, :, 2]
            row.append(np.mean(hue)) # Teinte moyenne
            row.append(np.mean(saturation)) # Saturation moyenne
            row.append(np.mean(value)) # Valeur moyenne
            row.append(np.median(hue)) # Teinte médiane
            row.append(np.median(saturation)) # Saturation médiane
            row.append(np.median(value)) # Valeur médianne
            # On ajoute la ligne
            data.append(row)
        except IOError: # Si l'image est illisible, on prévient l'utilisateur et passe à l'image suivante
            print(f"Cannot identify image file {name}")
            continue

    # On ouvre un fichier data.csv en écriture dans le dossier data, crée le dossier et le fichier s'ils n'existent pas
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(f"{OUTPUT_DIR}/data.csv", mode="w", newline="") as file:
        writer = csv.writer(file) # On crée un csv Writer et l'assigne au fichier
        writer.writerows(data) # On passe notre data dans le fichier


if __name__ == "__main__":
    main()