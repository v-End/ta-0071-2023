import os
import shutil

# Specify the folder path for the .vti files
folder_path = os.getcwd()

# Get a list of .vti files in the folder
files = [f for f in os.listdir(folder_path) if f.endswith('.vti')]

# Iterate over the .vti files
for file in files:
    # Extract the filename without extension
    filename = os.path.splitext(file)[0]

    # Create a folder with the filename if it doesn't exist
    folder_name = os.path.join(folder_path, filename)
    os.makedirs(folder_name, exist_ok=True)

    # Move the current .vti file into the folder
    source_path = os.path.join(folder_path, file)
    destination_path = os.path.join(folder_name, 'gprData.vti')
    shutil.move(source_path, destination_path)

    print(f"Moved {file} to {destination_path}")

print("All files processed.")