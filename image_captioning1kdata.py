# -*- coding: utf-8 -*-
"""
Created on Mon Feb  3 21:35:57 2025

@author: vicky
"""

import random
import os
import shutil

# Paths to the dataset and caption file
image_dir = r'C:\Users\vicky\Documents\image captioning\archive (13)\Images'  # Directory where images are stored
caption_file = r'C:\Users\vicky\Documents\image captioning\archive (13)\captions.txt'  # Caption file
selected_images_dir = r'C:\Users\vicky\Documents\image captioning\selected_images'  # Directory to save selected images
output_file = r'C:\Users\vicky\Documents\image captioning\selected_flickr8k_captions.txt'  # Output caption file

# Check if the caption file exists
print("Checking if the caption file exists:", os.path.exists(caption_file))

# Step 1: Read the caption file and store captions for each image
captions_dict = {}

with open(caption_file, 'r') as file:
    for line in file:
        line = line.strip()
        # Skip empty lines or improperly formatted lines
        if len(line.split(',')) == 2:  # Changed to split by comma
            image_id, caption = line.split(',', 1)  # Limit split to 2 parts
            if image_id not in captions_dict:
                captions_dict[image_id] = []
            captions_dict[image_id].append(caption)

# Debugging: Check if captions are being added
print(f"Total captions read: {len(captions_dict)}")  # Should print the number of unique image IDs

# Step 2: Check the number of available images
image_ids = list(captions_dict.keys())
num_images = len(image_ids)
print(f"Number of unique image IDs in the dataset: {num_images}")  # Debug: Number of unique images

# If there are less than 1000 images, adjust the sample size
sample_size = min(1000, num_images)

# Step 3: Randomly select images
selected_images = random.sample(image_ids, sample_size)

# Step 4: Create a new dictionary for the selected images and their captions
selected_captions = {image_id: captions_dict[image_id] for image_id in selected_images}

# Debugging: Check if selected images and captions are correctly stored
print(f"Number of selected images: {len(selected_captions)}")  # Should print the number of selected images

# Step 5: Create directory for selected images if it doesn't exist
if not os.path.exists(selected_images_dir):
    os.makedirs(selected_images_dir)

# Step 6: Copy selected images to the new directory
for image_id in selected_images:
    image_path = os.path.join(image_dir, image_id)
    if os.path.exists(image_path):  # Check if the image file exists
        shutil.copy(image_path, os.path.join(selected_images_dir, image_id))

# Step 7: Save the selected images and captions in a new file
with open(output_file, 'w') as output_file:
    for image_id, captions in selected_captions.items():
        for caption in captions:
            output_file.write(f"{image_id},{caption}\n")  # Save with comma separator

print(f"Selected {sample_size} images and their captions have been saved to '{output_file}'.")
print(f"Selected images have been copied to '{selected_images_dir}'.")

o 