import requests
import sys, os
import tkinter as tk
from tkinter import filedialog
import shutil

def create_config():
    """
    Creates a configuration file named 'config.txt' if it does not already exist.
    The function prompts the user to select two directories using a graphical file dialog:
    1. A folder to save the file.
    2. A folder to unpack the file.
    The selected directories are written to 'config.txt'. If no folder is selected, 
    a default path will be used (though this behavior is not explicitly defined in the function).
    Note:
        This function uses the 'os' and 'tkinter' modules, and requires a graphical 
        environment to display the file dialogs.
    """
    

    if not os.path.exists("config.txt"):
        with open("config.txt", "w") as f:
            root = tk.Tk()
            root.withdraw()  # Hide the main window

            folder_selected = filedialog.askdirectory(title="Select a folder to save the file")
            if folder_selected:
                f.write(f"{folder_selected}\n")
            else:
                print("No folder selected. Default path will be used.")
            
            folder_unpack = filedialog.askdirectory(title="Select a folder to unpack the file")
            if folder_unpack:
                f.write(f"{folder_unpack}\n")
            else:
                print("No folder selected. Default path will be used.")

def get_config():
    """
    Reads configuration settings from a file named 'config.txt'.
    The function opens 'config.txt' in read mode, reads its lines, and extracts
    the first two lines as configuration settings. It strips any leading or trailing
    whitespace from these lines and prints them to the console.
    Returns:
        tuple: A tuple containing two strings:
            - save: The first line from the configuration file.
            - unpack: The second line from the configuration file.
    """
    
    with open("config.txt", "r") as f:
        x = f.readlines()
        print(x)
        save = x[0].strip()
        print(save)
        unpack = x[1].strip()
        print(unpack)
        
        return save, unpack

# URL of the GitHub API for the latest release
repo_owner = "NeverSinkDev"
create_config()
folder_selected, folder_unpack = get_config()
repo_name = "NeverSink-PoE2litefilter"
api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest"

# Send request to the API
response = requests.get(api_url)
response.raise_for_status()  # Catch errors

# Parse JSON response
release_data = response.json()
print(release_data)

# Output information about the latest release
release_name = release_data.get("name", "Unnamed")
release_tag = release_data.get("tag_name", "Unnamed")
print(f"Latest release: {release_name} ({release_tag})")

# Search for assets
zipball = release_data.get("zipball_url")
print(f"ZIP file: {zipball}")
if not zipball:
    print("No assets found in the release.")
    exit()

# Find download URL of the ZIP file
download_url = zipball

# Download ZIP file
zip_response = requests.get(download_url, stream=True)
zip_response.raise_for_status()

# Save ZIP file
zip_file_name = "NeverSink-PoE2litefilter.zip"
print(f"Saving file to '{folder_selected}/{zip_file_name}'...")
with open(f"{folder_selected}/{zip_file_name}", "wb") as f:
    for chunk in zip_response.iter_content(chunk_size=8192):
        f.write(chunk)

print(f"File '{zip_file_name}' was successfully downloaded.")

def unpack_zip(unpack_folder):
    """
    Unpacks a ZIP file into the specified folder.
    Args:
        unpack_folder (str): The path to the folder where the contents of the ZIP file will be extracted.
    Raises:
        FileNotFoundError: If the ZIP file or the target folder does not exist.
        zipfile.BadZipFile: If the file is not a ZIP file or it is corrupted.
        OSError: If there is an error creating files in the target folder.
    Example:
        unpack_zip("/path/to/unpack/folder")
    """
    
    import zipfile

    with zipfile.ZipFile(f"{folder_selected}/{zip_file_name}", "r") as zip_ref:
        for member in zip_ref.namelist():
            filename = os.path.basename(member)
            if not filename:
                continue
            source = zip_ref.open(member)
            target = open(os.path.join(unpack_folder, filename), "wb")
            with source, target:
                shutil.copyfileobj(source, target)

    print("ZIP file has been unpacked.")

unpack_zip(folder_unpack)
