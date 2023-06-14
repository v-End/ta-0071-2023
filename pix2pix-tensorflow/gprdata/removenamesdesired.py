import os

# Specify the folder path
folder_path = ["desired/bordered", "desired/borderless"]

for idx, i in enumerate(folder_path):
    # Get a list of PNG files in the folder
    png_files = [f for f in os.listdir(i) if f.endswith('.png')]

    # Iterate over the PNG files
    for png_file in png_files:
        file_path = os.path.join(i, png_file)
        file_name, file_ext = os.path.splitext(png_file)

        if file_name.endswith('_geo_out'):
            new_file_name = file_name[:-8] + file_ext
        
        new_file_path = os.path.join(i, new_file_name)

        os.rename(file_path, new_file_path)
        print(f"Renamed '{png_file}' to '{new_file_name}'")

    print(f"{idx} Complete.")

print("Renaming complete.")