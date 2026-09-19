import os
import csv
import numpy as np
from PIL import Image
from tqdm import tqdm

IMAGE_DIR = "./images_720p" # Image folder to analyze (images, images_720p or images_480p)
OUTPUT_DIR = "./data" # Output folder for the csv

def main():
    # Define the csv structure with column headers
    data = [["name","width","height","aspectRatio","meanHue","meanSaturation","meanValue", "medianHue", "medianSaturation", "medianValue"]]
    files = os.listdir(IMAGE_DIR) # Get the images from the chosen folder, must be located next to main.py
    for name in tqdm(files, desc="Analyzing"): # For each file
        try:
            image = Image.open(f"{IMAGE_DIR}/{name}").convert("HSV") # Open the image in HSV format

            # Create a new row containing the name and add the data in order
            row = [name] # Name
            row.append(image.width) # Width
            row.append(image.height) # Height
            row.append(image.width / image.height) # Aspect ratio
            hsv_array = np.array(image)
            hue, saturation, value = hsv_array[:, :, 0], hsv_array[:, :, 1], hsv_array[:, :, 2]
            row.append(np.mean(hue)) # Mean hue
            row.append(np.mean(saturation)) # Mean saturation
            row.append(np.mean(value)) # Mean value
            row.append(np.median(hue)) # Median hue
            row.append(np.median(saturation)) # Median saturation
            row.append(np.median(value)) # Median value
            # Add the row
            data.append(row)
        except IOError: # If the image can't be read, warn the user and move to the next image
            print(f"Cannot identify image file {name}")
            continue

    print(f"Analyzed {len(data) - 1} images, {len(files) - (len(data) - 1)} failed.")

    # Open a data.csv file for writing in the data folder, created if it doesn't exist
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(f"{OUTPUT_DIR}/data.csv", mode="w", newline="") as file:
        writer = csv.writer(file) # Create a csv writer and assign it to the file
        writer.writerows(data) # Write our data to the file


if __name__ == "__main__":
    main()
