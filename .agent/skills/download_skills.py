import urllib.request
import json
import os

repo_url = "https://api.github.com/repos/sickn33/antigravity-awesome-skills/contents/skills"

def download_skill(skill_name, target_dir):
    url = f"{repo_url}/{skill_name}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Antigravity-Agent-IDE'})
    try:
        with urllib.request.urlopen(req) as response:
            files = json.loads(response.read().decode())
            os.makedirs(target_dir, exist_ok=True)
            for f in files:
                if f['type'] == 'file':
                    print(f"Descargando {f['name']} en {target_dir}...")
                    # Download file
                    file_req = urllib.request.Request(f['download_url'], headers={'User-Agent': 'Antigravity-Agent-IDE'})
                    with urllib.request.urlopen(file_req) as file_resp:
                        with open(os.path.join(target_dir, f['name']), 'wb') as out_file:
                            out_file.write(file_resp.read())
    except Exception as e:
        print(f"Error descargando {skill_name}: {e}")

global_dir = r"C:\Users\unive\.gemini\config\plugins\awesome-skills\skills"
local_dir = r"c:\Users\unive\OneDrive\Documentos\Proyectos\agente-urbanistico\.agent\skills"

skills_to_download = ['google-docs-automation', 'networkx']

for s in skills_to_download:
    print(f"\n--- Instalando {s} ---")
    download_skill(s, os.path.join(global_dir, s))
    download_skill(s, os.path.join(local_dir, s))
    
print("\nInstalacion completada.")
