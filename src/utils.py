import os
from tkinter import messagebox

def create_directories(path):
    """
    Create directories at the specified path, with error handling.

    :param path: The path where directories should be created
    """
    # Keep spaces and 'l' as they are, just create the directory
    try:
        os.makedirs(path, exist_ok=True)
    except Exception as e:
        messagebox.showerror("Error", f"Error creating directory {path}: {e}")
