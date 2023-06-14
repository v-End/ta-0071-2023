import os
import shutil

folder_path = 'input/'  # Replace with the actual folder path

up_amp_folder = os.path.join(folder_path, 'unprocessed/amp/')
os.makedirs(up_amp_folder, exist_ok=True)

up_freq_folder = os.path.join(folder_path, 'unprocessed/freq/')
os.makedirs(up_freq_folder, exist_ok=True)

p_amp_folder = os.path.join(folder_path, 'processed/amp/')
os.makedirs(p_amp_folder, exist_ok=True)

p_freq_folder = os.path.join(folder_path, 'processed/freq/')
os.makedirs(p_freq_folder, exist_ok=True)

# Get a list of PNG files in the folder
png_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.png')]
print(os.listdir())

# Iterate over the PNG files
for png_file in png_files:
    file_path = os.path.join(folder_path, png_file)
    file_name, file_ext = os.path.splitext(png_file)

    if file_name.endswith('_post'):
        if file_name.endswith('_frequency_post'):
            new_file_path = os.path.join(p_freq_folder, png_file)

            shutil.move(file_path, new_file_path)
            print(f"1 - Moved '{png_file}' to '{p_freq_folder}'")
        else:
            new_file_path = os.path.join(p_amp_folder, png_file)

            shutil.move(file_path, new_file_path)
            print(f"2 - Moved '{png_file}' to '{p_amp_folder}'")
    else:
        if file_name.endswith('_frequency'):
            new_file_path = os.path.join(up_freq_folder, png_file)

            shutil.move(file_path, new_file_path)
            print(f"3 - Moved '{png_file}' to '{up_freq_folder}'")
        else:
            new_file_path = os.path.join(up_amp_folder, png_file)

            shutil.move(file_path, new_file_path)
            print(f"4 - Moved '{png_file}' to '{up_amp_folder}'")

print("Moving files complete.")