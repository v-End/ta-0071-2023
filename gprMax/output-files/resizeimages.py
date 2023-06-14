import os
from PIL import Image

# Specify the folder path
folder_path = os.getcwd()

# Create the output folder if it doesn't exist
output_folder = os.path.join(folder_path, 'output')
os.makedirs(output_folder, exist_ok=True)

# Get a list of .png files in the folder
png_files = [f for f in os.listdir(folder_path) if f.endswith('.png')]

# Iterate over the .png files
for png_file in png_files:
    # Open the image using PIL
    image_path = os.path.join(folder_path, png_file)
    image = Image.open(image_path)

    # Resize the image to 256x256
    resized_image = image.resize((256, 256))

    # Save the resized image to the output folder
    output_path = os.path.join(output_folder, png_file)
    resized_image.save(output_path)

    print(f"Resized {png_file} and saved to {output_path}")

print("All images resized.")