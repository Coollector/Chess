import os
from PIL import Image

# Set the path to the folder containing the images
path = 'c:/Users/felix/Programmieren/Python/Chess/config/images'

# Iterate over the files in the folder
for filename in os.listdir(path):
    # Check if the file is an image
    if filename.endswith('.png') or filename.endswith('.jpg'):
        # Open the image file
        im = Image.open(os.path.join(path, filename))

        # Resize the image to 120x120 pixels
        im = im.resize((100, 100))

        # Save the resized image
        im.save(os.path.join(path, filename))
