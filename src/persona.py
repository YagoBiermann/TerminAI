import json
import os
from dotenv import load_dotenv

def load_file(path):
  try:
    with open(path, "r") as f:
      file = json.load(f)
      return file
    
  except FileNotFoundError:
      return None

load_dotenv()
file_path = os.path.dirname(os.path.abspath(__file__))
root_path = os.path.dirname(file_path)
persona_path = os.path.join(root_path, "personas.json")
personas = load_file(persona_path)

current_persona_key = os.getenv('CURRENT_PERSONA')
persona_description = ""

if personas and current_persona_key in personas:
    selected_persona = personas[current_persona_key]
    for key, value in selected_persona.items():
      persona_description += f"""{key}: {value}\n"""
else:
  print(f"Warning: Persona '{current_persona_key}' not applied. Using default settings")