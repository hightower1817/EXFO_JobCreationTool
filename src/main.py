import tkinter as tk
from tkinter import messagebox
import yaml
import os
import json
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src import config, gui, panels, utils

def main():
    # Load configuration from YAML file
    config_data = config.load_config()

    # Create main window
    root = tk.Tk()
    gui.setup_gui(root, config_data)

    # Function to handle Data Hall selection
    def select_data_hall(dh):
        panels.select_data_hall(dh, root, config_data)

    # Function to show panel
    def show_panel(panel_type, data_hall):
        panels.show_panel(panel_type, data_hall, root, config_data)

    # Here, root.mainloop() will be called by gui.setup_gui()
    # This ensures the GUI remains open and responsive

if __name__ == "__main__":
    main()
