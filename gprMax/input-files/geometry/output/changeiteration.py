import os
import shutil

# Specify the folder path
folder_path = os.getcwd()

# Get a list of PNG files in the folder
png_files = [f for f in os.listdir(folder_path) if f.endswith('.png')]

# Iterate over the PNG files
for png_file in png_files:
    # Split the filename into three parts
    a, b, c, d, e = png_file.split('_')
    
    # Check if the filename matches the expected format
    if a == 'RebarCorrosion':
        # Extract the 'num' part from the filename
        num = int(b[1:])
        
        # Add 100 to the 'num' part
        new_num = num + 120
        
        # Construct the new filename
        new_file_name = f"{a}_i{new_num}_{c}_{d}_{e}"
        
        # Construct the old and new file paths
        old_file_path = os.path.join(folder_path, png_file)
        new_file_path = os.path.join(folder_path, new_file_name)
        
        # Rename the file
        os.rename(old_file_path, new_file_path)
        
        print(f"Renamed file: {png_file} -> {new_file_name}")

print("File renaming completed.")
