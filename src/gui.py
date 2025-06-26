import tkinter as tk
from tkinter import ttk
from .panels import select_data_hall, show_panel
import yaml
from tkinter import messagebox
from auth import check_user, create_table

# Ensure the users table is created before the application starts
try:
    create_table()
except Exception as e:
    messagebox.showerror("Database Error", f"Failed to create or access user database: {e}")
    exit(1)

def load_config():
    try:
        with open('config.yaml', 'r') as file:
            return yaml.safe_load(file)
    except Exception as e:
        messagebox.showerror("Error", f"Error loading YAML configuration file: {e}")
        exit(1)

def setup_gui(root, config):
    # Set window properties
    root.geometry(f"{config['window']['width']}x{config['window']['height']}")
    root.title(config['window']['title'])
    
    # Configure font - using ttk for better style control
    style = ttk.Style()
    style.theme_use('clam')  # 'clam' theme looks cleaner, but you can customize or use others
    style.configure('TButton', font=(config['font']['type'], config['font']['size']), foreground=config['colors']['button_foreground'])
    style.configure('TLabel', font=(config['font']['type'], config['font']['size'] + config['ttk_styles']['label']['font_size_increase']), 
                    background=config['colors']['background'], foreground=config['colors']['foreground'])
    
    # Set background color
    root.configure(bg=config['colors']['background'])

    # Main frame
    main_frame = ttk.Frame(root, style='TFrame')
    main_frame.pack(expand=True, fill='both', padx=config['gui']['frame_padding'], pady=config['gui']['frame_padding'])

    # Top navigation for Data Hall selection
    top_nav = ttk.Frame(main_frame, style='DHMenuBar.TFrame')
    top_nav.pack(side=tk.TOP, fill=tk.X, pady=(config['gui']['frame_padding'], 0))
    
    style.configure('DHMenuBar.TFrame', background=config['colors']['dh_menu_bar'])

    # Configure styles for Data Hall buttons
    style.configure(config['gui']['dh_button_style'], 
                    padding=config['ttk_styles']['button']['padding'], 
                    relief=config['ttk_styles']['button']['relief'],
                    background=config['colors']['dh_button_background'], 
                    foreground=config['colors']['button_foreground'])
    style.map(config['gui']['dh_button_style'], 
              background=[('active', config['colors']['dh_button_hover_background'])])

    # Dropdown menu for Data Hall selection with default empty selection
    dh_var = tk.StringVar(top_nav)
    dh_var.set("DATA HALLS")  # Default to empty string
    
    # Updated: Use data_halls list from config
    dh_options = ["DATA HALLS"] + [dh['name'] for dh in config['gui']['data_halls']]
    
    dh_dropdown = ttk.OptionMenu(top_nav, dh_var, *dh_options, 
                                 command=lambda x: select_data_hall(x if x != "DATA HALLS" else None, main_frame, config))
    # Center the dropdown menu
    dh_dropdown.pack(anchor='center', expand=True)
    
    style.configure("TMenubutton", background=config['colors']['dh_button_background'], 
                    foreground=config['colors']['button_foreground'])
    style.map("TMenubutton", background=[('active', config['colors']['dh_button_hover_background'])])

    # No panel buttons here, they will be created in select_data_hall
    
    # Start with no Data Hall selected
    select_data_hall(None, main_frame, config)  # Call with None to indicate no selection

    # Keep the application running
    root.mainloop()

def login_window():
    login_root = tk.Tk()
    login_root.title("Login")
    login_root.geometry("300x200")

    ttk.Label(login_root, text="Username:").pack(pady=5)
    username_entry = ttk.Entry(login_root)
    username_entry.pack()

    ttk.Label(login_root, text="Password:").pack(pady=5)
    password_entry = ttk.Entry(login_root, show='*')
    password_entry.pack()

    def login():
        if check_user(username_entry.get(), password_entry.get()):
            login_root.destroy()
            root = tk.Tk()
            config = load_config()
            setup_gui(root, config)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    ttk.Button(login_root, text="Login", command=login).pack(pady=20)
    login_root.mainloop()

if __name__ == "__main__":
    login_window()
