import requests

# URL der GitHub API für das neueste Release
repo_owner = "NeverSinkDev"
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
with open(zip_file_name, "wb") as f:
    for chunk in zip_response.iter_content(chunk_size=8192):
        f.write(chunk)

print(f"Datei '{zip_file_name}' wurde erfolgreich heruntergeladen.")
