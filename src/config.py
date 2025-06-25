import yaml
from tkinter import messagebox

def load_config():
    try:
        with open('config.yaml', 'r') as file:
            return yaml.safe_load(file)
    except Exception as e:
        messagebox.showerror("Error", f"Error loading YAML configuration file: {e}")
        exit(1)
