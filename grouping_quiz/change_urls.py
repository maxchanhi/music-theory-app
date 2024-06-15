import os
from wrong_cat import urls
import time
def remove_spaces_from_png_filenames(directory):
    # Iterate through all files in the specified directory
    idx=0
    for filename in os.listdir(directory):
        # Check if the file is a PNG file and if it contains spaces
        old_filepath = os.path.join(directory, filename)
        new_filepath = os.path.join(directory, f"{idx}.png")
        # Rename the file
        os.rename(old_filepath, new_filepath)
        print(f'Renamed: {old_filepath} -> {new_filepath}')
        time.sleep(1)
        idx+=1


directory = f'static/beaming'
remove_spaces_from_png_filenames(directory)