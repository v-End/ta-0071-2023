import os
from PIL import Image

# Specify the folder path
folder_path = ["bordered", "borderless"]

for idx, iter in enumerate(folder_path):
    # Create the output folder if it doesn't exist
    output_folder = os.path.join(os.getcwd(), iter)
    os.makedirs(output_folder, exist_ok=True)

    # Get a list of .png files in the folder
    png_files = [f for f in os.listdir(os.getcwd()) if f.endswith('.png')]

    # Iterate over the .png files
    for png_file in png_files:
        # Open the image using PIL
        image_path = os.path.join(os.getcwd(), png_file)
        image = Image.open(image_path)

        # Crop the image to remove specified pixels from the edges (18, 78 = bordered) (52, 112 = borderless)
        if idx == 0:
            cropped_image = image.crop((18, 78, image.width - 18, image.height - 78))
        else:
            cropped_image = image.crop((52, 112, image.width - 52, image.height - 112))

        # Resize the cropped image to 256x256
        resized_image = cropped_image.resize((256, 256))

        # Save the resized image to the output folder
        output_path = os.path.join(output_folder, png_file)
        resized_image.save(output_path)

        print(f"Cropped and resized {png_file} and saved to {output_path}")

    print(f"{idx} Complete.")

print("All images cropped and resized.")