import requests
import sys, os
import tkinter as tk
from tkinter import filedialog
import shutil

def create_config():
    if not os.path.exists("config.txt"):
        with open("config.txt", "w") as f:
            root = tk.Tk()
            root.withdraw()  # Versteckt das Hauptfenster

            folder_selected = filedialog.askdirectory(title="Wählen Sie einen Ordner zum Speichern der Datei aus")
            if folder_selected:
                f.write(f"{folder_selected}\n")
            else:
                print("Kein Ordner ausgewählt. Standardpfad wird verwendet.")
            
            folder_unpack = filedialog.askdirectory(title="Wählen Sie einen Ordner zum Speichern der Datei aus")
            if folder_unpack:
                f.write(f"{folder_unpack}\n")
            else:
                print("Kein Ordner ausgewählt. Standardpfad wird verwendet.")

def get_config():
    with open("config.txt", "r") as f:
        x = f.readlines()
        print(x)
        save = x[0].strip()
        print(save)
        unpack = x[1].strip()
        print(unpack)
        
        return save, unpack

# URL der GitHub API für das neueste Release
repo_owner = "NeverSinkDev"
create_config()
folder_selected, folder_unpack = get_config()
repo_name = "NeverSink-PoE2litefilter"
api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest"

# Anfrage an die API senden
response = requests.get(api_url)
response.raise_for_status()  # Fehler abfangen

# JSON-Antwort analysieren
release_data = response.json()
print(release_data)

# Informationen zum neuesten Release ausgeben
release_name = release_data.get("name", "Unbenannt")
release_tag = release_data.get("tag_name", "Unbenannt")
print(f"Neuestes Release: {release_name} ({release_tag})")

# Suche nach Assets
zipball = release_data.get("zipball_url")
print(f"ZIP-Datei: {zipball}")
if not zipball:
    print("Keine Assets im Release gefunden.")
    exit()

# Download-URL der ZIP-Datei finden


download_url = zipball

# ZIP-Datei herunterladen
zip_response = requests.get(download_url, stream=True)
zip_response.raise_for_status()

# ZIP-Datei speichern
zip_file_name = "NeverSink-PoE2litefilter.zip"
print(f"Speichere Datei in '{folder_selected}/{zip_file_name}'...")
with open(f"{folder_selected}/{zip_file_name}", "wb") as f:
    for chunk in zip_response.iter_content(chunk_size=8192):
        f.write(chunk)

print(f"Datei '{zip_file_name}' wurde erfolgreich heruntergeladen.")





def unpack_zip(unpack_folder):
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

    print("ZIP-Datei wurde entpackt.")

unpack_zip(folder_unpack)