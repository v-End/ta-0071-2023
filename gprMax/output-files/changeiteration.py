import os
import shutil

# Specify the folder path
folder_path = os.getcwd()

# Get a list of PNG files in the folder
png_files = [f for f in os.listdir(folder_path) if f.endswith('.png')]

# Iterate over the PNG files
for png_file in png_files:
    # Split the filename into three parts
    str = png_file.split('_')

    # Check if the filename matches the expected format
    if str[0] == 'RebarCorrosion':
        # Extract the 'num' part from the filename
        num = int(str[1][1:]) + 120

        new_file_name = ""

        # Construct the new filename
        if len(str) == 4:
            new_file_name = f"{str[0]}_i{num}_{str[2]}_{str[3]}"
        elif len(str) == 5:
            new_file_name = f"{str[0]}_i{num}_{str[2]}_{str[3]}_{str[4]}"
        elif len(str) == 6:
            new_file_name = f"{str[0]}_i{num}_{str[2]}_{str[3]}_{str[4]}_{str[5]}"

        # Construct the old and new file paths
        old_file_path = os.path.join(folder_path, png_file)
        new_file_path = os.path.join(folder_path, new_file_name)

        # Rename the file
        os.rename(old_file_path, new_file_path)

        print(f"Renamed file: {png_file} -> {new_file_name}")

print("File renaming completed.")
