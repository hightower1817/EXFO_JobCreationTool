import tkinter as tk
from tkinter import messagebox
import os
import json
import yaml
from tkinter import ttk

# Load configuration from YAML file
with open('config.yaml', 'r') as ymlfile:
    config = yaml.safe_load(ymlfile)

def create_directories(path):
    os.makedirs(path, exist_ok=True)

# panels.py

def select_data_hall(dh, main_frame, config):
    # Clear existing widgets except for navigation or persistent elements
    for widget in main_frame.winfo_children():
        if widget.winfo_class() != "TFrame":  # Only clear if not the top navigation frame
            widget.destroy()
    
    if dh is None:
        # If no data hall is selected, just show a message or nothing
        content = ttk.Frame(main_frame, style='Content.TFrame')
        content.pack(side=tk.TOP, expand=True, fill='both', 
                     padx=config['gui']['content_padding'], pady=config['gui']['content_padding'])
        
        ttk.Label(content, text="Please select a Data Hall", style='TLabel').pack()
    else:
        content = ttk.Frame(main_frame, style='Content.TFrame')
        content.pack(side=tk.TOP, expand=True, fill='both', 
                     padx=config['gui']['content_padding'], pady=config['gui']['content_padding'])
        
        # Label for the current Data Hall
        ttk.Label(content, text=f"Data Hall {dh}", style='TLabel').pack()

        # Create panel buttons
        panels = ['AS-T1', 'GPU-T1', 'RT1-RT2', 'RT2-RT3', 'SIST1-T2']
        panel_nav = ttk.Frame(content, style='PanelMenuBar.TFrame')
        panel_nav.pack(side=tk.TOP, fill=tk.X, pady=(0, config['gui']['frame_padding']))
        
        style = ttk.Style()
        
        style.configure('Uniform.TButton', 
                        width=config['gui']['panel_buttons']['width'], 
                        height=config['gui']['panel_buttons']['height'],
                        padding=config['ttk_styles']['button']['padding'], 
                        relief=config['ttk_styles']['button']['relief'],
                        background=config['colors']['panel_button_background'], 
                        foreground=config['colors']['button_foreground'])
        style.map('Uniform.TButton', 
                  background=[('active', config['colors']['panel_button_hover_background'])])

        for panel in panels:
            button = ttk.Button(panel_nav, text=panel, 
                                command=lambda p=panel, hall=dh: show_panel(p, hall, content, config),
                                style='Uniform.TButton')
            button.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=2, pady=2)

def show_panel(panel_type, data_hall, content, config):
    for widget in content.winfo_children():
        widget.destroy()
    
    panel_functions = {
        'AS-T1': show_as_t1_panel,
        'GPU-T1': show_gpu_t1_panel,
        'RT1-RT2': show_rt1_rt2_panel,
        'RT2-RT3': show_rt2_rt3_panel,
        'SIST1-T2': show_sist1_t2_panel
    }
    
    if panel_type in panel_functions:
        panel_functions[panel_type](data_hall, content, config)
    else:
        messagebox.showinfo("Info", f"{panel_type} panel not implemented yet.")

def show_as_t1_panel(data_hall, content, config):
    style = ttk.Style()
    style.configure('SubPanel.TButton', 
                    width=config['gui']['panel_buttons']['width'], 
                    height=config['gui']['panel_buttons']['height'],
                    padding=config['ttk_styles']['button']['padding'], 
                    relief=config['ttk_styles']['button']['relief'],
                    background=config['colors']['panel_button_background'], 
                    foreground=config['colors']['button_foreground'])
    style.map('SubPanel.TButton', 
              background=[('active', config['colors']['panel_button_hover_background'])])

    for i, nb in enumerate(config['as_t1']['nb_options'], start=1):
        row = (i - 1) // 4  # Assuming 4 buttons per row, adjust as needed
        col = (i - 1) % 4
        ttk.Button(content, text=nb, 
                   command=lambda n=nb, hall=data_hall: create_as_t1_directories(n, hall, config),
                   style='SubPanel.TButton').grid(row=row, column=col, padx=2, pady=2)

def create_as_t1_directories(nb, data_hall, config):
    base_path = os.path.join("Jobs/AS-T1", nb)  # AS-T1/NB##
    create_directories(base_path)  # Show success message for base directory
    
    for dir in config['as_t1']['nb_to_dirs'][nb]:
        original_path = f"(as)SIS-T1 l DH{data_hall} {nb} {dir}"
        full_path = os.path.join(base_path, original_path)
        create_directories(full_path)  # No success message for these directories
        
        # Create info.json for AS-T1
        d_num, b_num = dir.split()
        info_data = {
            "Name":f"(as)SIS-T1 l DH{data_hall} {nb} {d_num} {b_num}",
            "Min":f"{nb}-{b_num}-{d_num}-{config['constants']['as_t1_min_suffix']}",
            "Max":f"{nb}-{b_num}-{d_num}-{config['constants']['as_t1_max_suffix']}",
            "Operator":"",
            "Company":"",
            "Customer":""
        }
        with open(os.path.join(full_path, 'info.json'), 'w') as f:
            json.dump(info_data, f, indent=None, separators=(',', ':'))

def show_gpu_t1_panel(data_hall, content, config):
    style = ttk.Style()
    style.configure('SubPanel.TButton', 
                    width=config['gui']['panel_buttons']['width'], 
                    height=config['gui']['panel_buttons']['height'],
                    padding=config['ttk_styles']['button']['padding'], 
                    relief=config['ttk_styles']['button']['relief'],
                    background=config['colors']['panel_button_background'], 
                    foreground=config['colors']['button_foreground'])
    style.map('SubPanel.TButton', 
              background=[('active', config['colors']['panel_button_hover_background'])])

    for i, su in enumerate(range(1, config['SU_panel']['button_count'] + 1), start=1):
        su_str = f"{config['SU_panel']['prefix']}{su:02d}"
        row = (i - 1) // 8  # Assuming 8 buttons per row, adjust as needed
        col = (i - 1) % 8
        ttk.Button(content, text=su_str, 
                   command=lambda s=su_str, hall=data_hall: create_gpu_t1_directories(s, hall, config),
                   style='SubPanel.TButton').grid(row=row, column=col, padx=2, pady=2)


def create_gpu_t1_directories(su, data_hall, config):
    base_path = "Jobs/GPU-T1"
    su_path = os.path.join(base_path, su)  # GPU-T1/SU##
    create_directories(su_path)  # Show success message for SU directory
    
    for rail in range(1, config['SU_panel']['rail_count'] + 1):
        rail_str = f"{config['SU_panel']['rail_prefix']}{rail}"
        dir_path = f"GPU-T1 l DH{data_hall} {su} {rail_str}"
        full_path = os.path.join(su_path, dir_path)
        create_directories(full_path)  # No success message for these directories
        
        # Extract the three-digit code for the SU from config
        su_code = config['su_to_code'].get(su, "000")  # Default to "000" if not found
        
        # Create info.json for GPU-T1 with the correct SU code
        info_data = {
            "Name":f"GPU-T1 l DH{data_hall} {su} {rail_str}",
            "Min":f"{su_code}-R{rail}-{config['constants']['gpu_t1_min_suffix']}",
            "Max":f"{su_code}-R{rail}-{config['constants']['gpu_t1_max_suffix']}",
            "Operator":"",
            "Company":"",
            "Customer":""
        }
        with open(os.path.join(full_path, 'info.json'), 'w') as f:
            json.dump(info_data, f, indent=4, separators=(',', ':'))
            
def show_rt1_rt2_panel(data_hall, content, config):
    style = ttk.Style()
    style.configure('SubPanel.TButton', 
                    width=config['gui']['panel_buttons']['width'], 
                    height=config['gui']['panel_buttons']['height'],
                    padding=config['ttk_styles']['button']['padding'], 
                    relief=config['ttk_styles']['button']['relief'],
                    background=config['colors']['panel_button_background'], 
                    foreground=config['colors']['button_foreground'])
    style.map('SubPanel.TButton', 
              background=[('active', config['colors']['panel_button_hover_background'])])

    for i, rail in enumerate(range(1, config['RT_panel']['button_count'] + 1), start=1):
        rail_str = f"{config['RT_panel']['prefix']}{rail}"
        row = (i - 1) // 4  # Adjust based on desired layout
        col = (i - 1) % 4
        ttk.Button(content, text=rail_str, 
                   command=lambda r=rail_str, hall=data_hall: create_rt1_rt2_directories(r, hall, config),
                   style='SubPanel.TButton').grid(row=row, column=col, padx=2, pady=2)

def create_rt1_rt2_directories(rail, data_hall, config):
    base_path = "Jobs/RT1-RT2"
    rail_path = os.path.join(base_path, rail)  # RT1-RT2/RAIL##
    create_directories(rail_path)  # Show success message for RAIL directory
    
    for su in range(1, config['RT_panel']['su_count'] + 1):
        su_str = f"SU{su}"
        dir_path = f"RT1-RT2 l DH{data_hall} {su_str} {rail}"
        full_path = os.path.join(rail_path, dir_path)
        create_directories(full_path)  # No success message for these directories
        
        # Extract the three-letter code for the SU from config
        su_code = config['su_to_code'].get(su_str, "000")  # Default to "000" if not found
        
        # Create info.json for RT1-RT2 with the correct SU code
        info_data = {
            "Name":f"RT1-RT2 l DH{data_hall} {su_str} {rail}",
            "Min":f"{su_code}-R{rail[4:]}-{config['constants']['rt1_rt2_min_suffix']}",
            "Max":f"{su_code}-R{rail[4:]}-{config['constants']['rt1_rt2_max_suffix']}",
            "Operator":"",
            "Company":"",
            "Customer":""
        }
        with open(os.path.join(full_path, 'info.json'), 'w') as f:
            json.dump(info_data, f, indent=4, separators=(',', ':'))

def show_rt2_rt3_panel(data_hall, content, config):
    style = ttk.Style()
    style.configure('SubPanel.TButton', 
                    width=config['gui']['panel_buttons']['width'], 
                    height=config['gui']['panel_buttons']['height'],
                    padding=config['ttk_styles']['button']['padding'], 
                    relief=config['ttk_styles']['button']['relief'],
                    background=config['colors']['panel_button_background'], 
                    foreground=config['colors']['button_foreground'])
    style.map('SubPanel.TButton', 
              background=[('active', config['colors']['panel_button_hover_background'])])

    for i, na in enumerate(config['RT2_RT3_panel']['na_options'], start=1):
        row = (i - 1) // 4  # Adjust based on how many you want per row
        col = (i - 1) % 4
        ttk.Button(content, text=na, 
                   command=lambda n=na, hall=data_hall: create_rt2_rt3_directories(n, hall, config),
                   style='SubPanel.TButton').grid(row=row, column=col, padx=2, pady=2)

def create_rt2_rt3_directories(na, data_hall, config):
    base_path = os.path.join("Jobs/RT2-RT3", "CNR3", na)
    create_directories(base_path)  # Show success message for base directory
    
    for na_group in config['RT2_RT3_panel']['na_to_dirs']:
        if na == na_group or int(na[-2:]) in config['RT2_RT3_panel']['na_to_dirs'][na_group]:
            group_index = list(config['RT2_RT3_panel']['na_to_dirs'].keys()).index(na_group)
            range_start = config['RT2_RT3_panel']['dir_ranges'][group_index]['start']
            range_end = config['RT2_RT3_panel']['dir_ranges'][group_index]['end']
            
            for d in range(range_start, range_end + 1):
                dir_path = f"RT2-RT3 l DH{data_hall} CNR3 {na} D{d}"
                full_path = os.path.join(base_path, dir_path)
                create_directories(full_path)  # Create lowest level directories without success messages
                
                # Create info.json for RT2-RT3
                info_data = {
                    "Name":f"RT2-RT3 l DH{data_hall} CNR3 {na} D{d}",
                    "Min":f"{na}-D{d}-{config['constants']['rt2_rt3_min_suffix']}",
                    "Max":f"{na}-D{d}-{config['constants']['rt2_rt3_max_suffix']}",
                    "Operator":"",
                    "Company":"",
                    "Customer":""
                }
                with open(os.path.join(full_path, 'info.json'), 'w') as f:
                    json.dump(info_data, f, indent=4, separators=(',', ':'))

def show_sist1_t2_panel(data_hall, content, config):
    style = ttk.Style()
    style.configure('SubPanel.TButton', 
                    width=config['gui']['panel_buttons']['width'], 
                    height=config['gui']['panel_buttons']['height'],
                    padding=config['ttk_styles']['button']['padding'], 
                    relief=config['ttk_styles']['button']['relief'],
                    background=config['colors']['panel_button_background'], 
                    foreground=config['colors']['button_foreground'])
    style.map('SubPanel.TButton', 
              background=[('active', config['colors']['panel_button_hover_background'])])

    for i, nc in enumerate(config['sist1_t2']['nc_options'], start=1):
        row = (i - 1) // 4  # Adjust based on how many you want per row
        col = (i - 1) % 4
        ttk.Button(content, text=nc, 
                   command=lambda n=nc, hall=data_hall: create_sist1_t2_directories(n, hall, config),
                   style='SubPanel.TButton').grid(row=row, column=col, padx=2, pady=2)

def create_sist1_t2_directories(nc, data_hall, config):
    base_path = os.path.join("Jobs/SIST1-T2", nc)
    create_directories(base_path)  # Create the NB directory
    
    for dir in config['sist1_t2']['nc_to_dirs'][nc]:
        parts = dir.split()
        b_num, d_num = parts[1], parts[0]
        full_path = f"SIST1-SIST2 l DH{data_hall} {nc} {b_num} {d_num}"
        full_path = os.path.join(base_path, full_path)
        create_directories(full_path)
        
        # Create info.json for SIST1-T2
        info_data = {
            "Name":f"SIST1-SIST2 l DH{data_hall} {nc} {b_num} {d_num}",
            "Min":f"{nc}-{b_num}-{d_num}-{config['constants']['sist1_t2_min_suffix']}",
            "Max":f"{nc}-{b_num}-{d_num}-{config['constants']['sist1_t2_max_suffix']}",
            "Operator":"",
            "Company":"",
            "Customer":""
        }
        with open(os.path.join(full_path, 'info.json'), 'w') as f:
            json.dump(info_data, f, indent=4, separators=(',', ':'))
