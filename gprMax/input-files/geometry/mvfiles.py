import os
import shutil

# Specify the folder path
folder_path = os.getcwd()

# Get a list of folders in the folder_path
folders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]

# Filter for folders starting with "RebarCorrosion_"
filtered_folders = [f for f in folders if f.startswith('RebarCorrosion_')]

# Iterate over the filtered folders
for folder in filtered_folders:
    # Get a list of .png files in the current folder
    png_files = [f for f in os.listdir(os.path.join(folder_path, folder)) if f.endswith('.png')]

    # Move each .png file to the 'output' folder
    for png_file in png_files:
        current_path = os.path.join(folder_path, folder, png_file)
        new_path = os.path.join(folder_path, 'output', png_file)
        shutil.move(current_path, new_path)
        print(f"Moved {png_file} to {os.path.join(folder_path, 'geometry', 'output')}")

print("All files processed.")