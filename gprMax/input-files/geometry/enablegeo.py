import os

folder_path = os.getcwd()  # Get the current folder path
file_extension = '.in'  # Specify the file extension

for filename in os.listdir(folder_path):
    if filename.endswith(file_extension):
        file_path = os.path.join(folder_path, filename)
        with open(file_path, 'r') as file:
            lines = file.readlines()
        
        with open(file_path, 'w') as file:
            for line in lines:
                modified_line = line.replace('--#geometry_view', '#geometry_view')
                file.write(modified_line)
        
        print(f"Modified {filename}")