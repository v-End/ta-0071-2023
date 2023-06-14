import os

# Specify the folder path
folder_path = ["input/processed/amp", "input/processed/freq", "input/unprocessed/amp", "input/unprocessed/freq"]

for idx, i in enumerate(folder_path):
    # Get a list of PNG files in the folder
    png_files = [f for f in os.listdir(i) if f.endswith('.png')]

    # Iterate over the PNG files
    for png_file in png_files:
        file_path = os.path.join(i, png_file)
        file_name, file_ext = os.path.splitext(png_file)

        if file_name.endswith('__frequency_post'):
            new_file_name = file_name[:-16] + file_ext
        elif file_name.endswith('__post'):
            new_file_name = file_name[:-6] + file_ext
        elif file_name.endswith('__frequency'):
            new_file_name = file_name[:-11] + file_ext
        elif file_name.endswith('_'):
            new_file_name = file_name[:-1] + file_ext
        
        new_file_path = os.path.join(i, new_file_name)

        os.rename(file_path, new_file_path)
        print(f"Renamed '{png_file}' to '{new_file_name}'")

    print(f"{idx} Complete.")

print("Renaming complete.")