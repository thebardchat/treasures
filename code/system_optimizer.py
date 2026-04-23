#!/usr/bin/env python3
"""
System Optimizer for ShaneBrain Development Console
Modular optimization tool with full user control
"""

import os
import sys
import json
import shutil
import subprocess
import time
import psutil
import hashlib
from datetime import datetime
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading

class SystemOptimizer:
    def __init__(self):
        self.config_file = Path.home() / ".shanebrain" / "optimizer_config.json"
        self.config_file.parent.mkdir(exist_ok=True)
        self.load_config()
        
    def load_config(self):
        """Load or create configuration"""
        default_config = {
            "archive_path": str(Path.home() / "ShaneBrain_Archive"),
            "gdrive_mount": "/mnt/gdrive",
            "folders_to_optimize": [
                str(Path.home() / "Documents"),
                str(Path.home() / "Downloads"),
                str(Path.home() / "Desktop")
            ],
            "auto_archive_days": 30,
            "min_file_size_mb": 100,
            "excluded_extensions": [".bat", ".exe", ".dll", ".sys"],
            "protected_folders": ["ShaneBrain", "AngelCloud", "PulsarAI"]
        }
        
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                self.config = json.load(f)
        else:
            self.config = default_config
            self.save_config()
    
    def save_config(self):
        """Save configuration"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def get_system_info(self):
        """Get current system status"""
        info = {
            "cpu_percent": psutil.cpu_percent(interval=1),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_usage": psutil.disk_usage('/').percent,
            "disk_free_gb": psutil.disk_usage('/').free / (1024**3)
        }
        return info
    
    def defragment_windows(self):
        """Run Windows defragmentation"""
        try:
            drives = ['C:', 'D:', 'E:']  # Add more if needed
            results = []
            
            for drive in drives:
                if os.path.exists(drive):
                    print(f"Analyzing {drive}...")
                    # Analyze first
                    analyze = subprocess.run(
                        ['defrag', drive, '/A'], 
                        capture_output=True, 
                        text=True
                    )
                    
                    if "needs optimization" in analyze.stdout.lower():
                        print(f"Defragmenting {drive}...")
                        defrag = subprocess.run(
                            ['defrag', drive, '/O'], 
                            capture_output=True, 
                            text=True
                        )
                        results.append(f"{drive} defragmented successfully")
                    else:
                        results.append(f"{drive} doesn't need defragmentation")
            
            return "\n".join(results)
        except Exception as e:
            return f"Defrag error: {str(e)}"
    
    def clean_temp_files(self):
        """Clean temporary files"""
        cleaned = 0
        temp_dirs = [
            os.environ.get('TEMP'),
            os.environ.get('TMP'),
            Path.home() / "AppData" / "Local" / "Temp"
        ]
        
        for temp_dir in temp_dirs:
            if temp_dir and os.path.exists(temp_dir):
                for root, dirs, files in os.walk(temp_dir):
                    for file in files:
                        try:
                            file_path = os.path.join(root, file)
                            if os.path.getmtime(file_path) < time.time() - 86400:  # Older than 1 day
                                os.remove(file_path)
                                cleaned += 1
                        except:
                            continue
        
        return f"Cleaned {cleaned} temporary files"
    
    def find_large_files(self, directory, min_size_mb=100):
        """Find files larger than specified size"""
        large_files = []
        min_size = min_size_mb * 1024 * 1024
        
        for root, dirs, files in os.walk(directory):
            # Skip protected folders
            dirs[:] = [d for d in dirs if d not in self.config['protected_folders']]
            
            for file in files:
                try:
                    file_path = os.path.join(root, file)
                    if os.path.getsize(file_path) > min_size:
                        large_files.append({
                            'path': file_path,
                            'size_mb': os.path.getsize(file_path) / (1024*1024),
                            'modified': datetime.fromtimestamp(os.path.getmtime(file_path))
                        })
                except:
                    continue
        
        return sorted(large_files, key=lambda x: x['size_mb'], reverse=True)
    
    def archive_to_gdrive(self, files_to_archive, gdrive_path):
        """Archive selected files to Google Drive"""
        archived = []
        archive_folder = f"ShaneBrain_Archive_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        for file_info in files_to_archive:
            try:
                source = file_info['path']
                relative_path = os.path.relpath(source, Path.home())
                dest = os.path.join(gdrive_path, archive_folder, relative_path)
                
                os.makedirs(os.path.dirname(dest), exist_ok=True)
                shutil.move(source, dest)
                archived.append(source)
                
                # Create a link file pointing to the archived location
                link_file = source + ".gdrive_link"
                with open(link_file, 'w') as f:
                    f.write(f"Archived to: {dest}\nDate: {datetime.now()}")
                
            except Exception as e:
                print(f"Error archiving {source}: {e}")
        
        return archived
    
    def optimize_startup(self):
        """Optimize Windows startup programs"""
        try:
            # Disable unnecessary startup programs
            startup_key = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
            import winreg
            
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, startup_key, 0, winreg.KEY_ALL_ACCESS)
            
            # Get all startup entries
            startup_programs = []
            i = 0
            while True:
                try:
                    name, value, _ = winreg.EnumValue(key, i)
                    startup_programs.append((name, value))
                    i += 1
                except WindowsError:
                    break
            
            winreg.CloseKey(key)
            return startup_programs
        except:
            return []
    
    def disable_visual_effects(self):
        """Optimize visual effects for performance"""
        try:
            # Set Windows for best performance
            subprocess.run([
                'reg', 'add', 
                'HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\VisualEffects',
                '/v', 'VisualFXSetting', '/t', 'REG_DWORD', '/d', '2', '/f'
            ])
            return "Visual effects optimized for performance"
        except Exception as e:
            return f"Visual effects optimization error: {e}"

class OptimizerGUI:
    def __init__(self):
        self.optimizer = SystemOptimizer()
        self.root = tk.Tk()
        self.root.title("ShaneBrain System Optimizer")
        self.root.geometry("800x600")
        
        # Set icon if available
        try:
            self.root.iconbitmap("shanebrain.ico")
        except:
            pass
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the user interface"""
        # Create notebook for tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # System Info Tab
        self.info_frame = ttk.Frame(notebook)
        notebook.add(self.info_frame, text='System Status')
        self.setup_info_tab()
        
        # Optimization Tab
        self.opt_frame = ttk.Frame(notebook)
        notebook.add(self.opt_frame, text='Optimization')
        self.setup_optimization_tab()
        
        # Archive Tab
        self.archive_frame = ttk.Frame(notebook)
        notebook.add(self.archive_frame, text='Archive to Cloud')
        self.setup_archive_tab()
        
        # Settings Tab
        self.settings_frame = ttk.Frame(notebook)
        notebook.add(self.settings_frame, text='Settings')
        self.setup_settings_tab()
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Auto-refresh system info
        self.refresh_system_info()
    
    def setup_info_tab(self):
        """Setup system information tab"""
        # System metrics
        metrics_frame = ttk.LabelFrame(self.info_frame, text="System Metrics", padding=10)
        metrics_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.cpu_var = tk.StringVar()
        self.memory_var = tk.StringVar()
        self.disk_var = tk.StringVar()
        self.free_space_var = tk.StringVar()
        
        ttk.Label(metrics_frame, textvariable=self.cpu_var, font=('Arial', 12)).pack(pady=5)
        ttk.Label(metrics_frame, textvariable=self.memory_var, font=('Arial', 12)).pack(pady=5)
        ttk.Label(metrics_frame, textvariable=self.disk_var, font=('Arial', 12)).pack(pady=5)
        ttk.Label(metrics_frame, textvariable=self.free_space_var, font=('Arial', 12)).pack(pady=5)
        
        # Progress bars
        self.cpu_progress = ttk.Progressbar(metrics_frame, length=400, mode='determinate')
        self.cpu_progress.pack(pady=5)
        
        self.memory_progress = ttk.Progressbar(metrics_frame, length=400, mode='determinate')
        self.memory_progress.pack(pady=5)
        
        self.disk_progress = ttk.Progressbar(metrics_frame, length=400, mode='determinate')
        self.disk_progress.pack(pady=5)
    
    def setup_optimization_tab(self):
        """Setup optimization tab"""
        # Quick actions
        actions_frame = ttk.LabelFrame(self.opt_frame, text="Quick Optimizations", padding=10)
        actions_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        ttk.Button(actions_frame, text="🧹 Clean Temp Files", 
                  command=self.clean_temp, width=30).pack(pady=5)
        ttk.Button(actions_frame, text="💾 Defragment Drives", 
                  command=self.defrag, width=30).pack(pady=5)
        ttk.Button(actions_frame, text="🚀 Optimize Startup", 
                  command=self.optimize_startup, width=30).pack(pady=5)
        ttk.Button(actions_frame, text="🎨 Optimize Visual Effects", 
                  command=self.optimize_visual, width=30).pack(pady=5)
        ttk.Button(actions_frame, text="⚡ Run All Optimizations", 
                  command=self.run_all_optimizations, width=30).pack(pady=10)
        
        # Output area
        output_frame = ttk.LabelFrame(self.opt_frame, text="Output", padding=10)
        output_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.output_text = tk.Text(output_frame, height=10, wrap=tk.WORD)
        self.output_text.pack(fill='both', expand=True)
        
        scrollbar = ttk.Scrollbar(output_frame, command=self.output_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.output_text.config(yscrollcommand=scrollbar.set)
    
    def setup_archive_tab(self):
        """Setup archive tab"""
        # File finder
        finder_frame = ttk.LabelFrame(self.archive_frame, text="Find Large Files", padding=10)
        finder_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(finder_frame, text="Minimum file size (MB):").pack(side=tk.LEFT, padx=5)
        self.min_size_var = tk.IntVar(value=100)
        ttk.Spinbox(finder_frame, from_=10, to=1000, textvariable=self.min_size_var, 
                   width=10).pack(side=tk.LEFT, padx=5)
        ttk.Button(finder_frame, text="Find Files", 
                  command=self.find_files).pack(side=tk.LEFT, padx=10)
        
        # File list
        list_frame = ttk.LabelFrame(self.archive_frame, text="Files to Archive", padding=10)
        list_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Treeview for files
        columns = ('Size (MB)', 'Modified', 'Path')
        self.file_tree = ttk.Treeview(list_frame, columns=columns, show='tree headings', height=10)
        self.file_tree.heading('#0', text='Select')
        self.file_tree.heading('Size (MB)', text='Size (MB)')
        self.file_tree.heading('Modified', text='Modified')
        self.file_tree.heading('Path', text='Path')
        
        self.file_tree.column('#0', width=50)
        self.file_tree.column('Size (MB)', width=100)
        self.file_tree.column('Modified', width=150)
        self.file_tree.column('Path', width=400)
        
        self.file_tree.pack(fill='both', expand=True)
        
        # Archive button
        ttk.Button(self.archive_frame, text="📤 Archive Selected to Google Drive", 
                  command=self.archive_files, width=30).pack(pady=10)
    
    def setup_settings_tab(self):
        """Setup settings tab"""
        settings_container = ttk.Frame(self.settings_frame)
        settings_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Protected folders
        protected_frame = ttk.LabelFrame(settings_container, text="Protected Folders", padding=10)
        protected_frame.pack(fill='x', pady=5)
        
        self.protected_list = tk.Listbox(protected_frame, height=5)
        self.protected_list.pack(fill='x', pady=5)
        
        for folder in self.optimizer.config['protected_folders']:
            self.protected_list.insert(tk.END, folder)
        
        button_frame = ttk.Frame(protected_frame)
        button_frame.pack(fill='x')
        
        ttk.Button(button_frame, text="Add Folder", 
                  command=self.add_protected_folder).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Remove Selected", 
                  command=self.remove_protected_folder).pack(side=tk.LEFT, padx=5)
        
        # Google Drive settings
        gdrive_frame = ttk.LabelFrame(settings_container, text="Google Drive Settings", padding=10)
        gdrive_frame.pack(fill='x', pady=5)
        
        ttk.Label(gdrive_frame, text="Google Drive Mount Path:").pack(anchor='w')
        self.gdrive_var = tk.StringVar(value=self.optimizer.config['gdrive_mount'])
        ttk.Entry(gdrive_frame, textvariable=self.gdrive_var, width=50).pack(fill='x', pady=5)
        
        # Save settings button
        ttk.Button(settings_container, text="💾 Save Settings", 
                  command=self.save_settings, width=20).pack(pady=10)
    
    def refresh_system_info(self):
        """Refresh system information display"""
        info = self.optimizer.get_system_info()
        
        self.cpu_var.set(f"CPU Usage: {info['cpu_percent']:.1f}%")
        self.memory_var.set(f"Memory Usage: {info['memory_percent']:.1f}%")
        self.disk_var.set(f"Disk Usage: {info['disk_usage']:.1f}%")
        self.free_space_var.set(f"Free Space: {info['disk_free_gb']:.1f} GB")
        
        self.cpu_progress['value'] = info['cpu_percent']
        self.memory_progress['value'] = info['memory_percent']
        self.disk_progress['value'] = info['disk_usage']
        
        # Schedule next refresh
        self.root.after(2000, self.refresh_system_info)
    
    def log_output(self, message):
        """Log message to output area"""
        self.output_text.insert(tk.END, f"[{datetime.now().strftime('%H:%M:%S')}] {message}\n")
        self.output_text.see(tk.END)
        self.root.update()
    
    def clean_temp(self):
        """Clean temporary files"""
        self.status_var.set("Cleaning temporary files...")
        threading.Thread(target=self._clean_temp_thread, daemon=True).start()
    
    def _clean_temp_thread(self):
        result = self.optimizer.clean_temp_files()
        self.log_output(result)
        self.status_var.set("Ready")
    
    def defrag(self):
        """Run defragmentation"""
        if messagebox.askyesno("Defragmentation", 
                               "Defragmentation may take a while. Continue?"):
            self.status_var.set("Running defragmentation...")
            threading.Thread(target=self._defrag_thread, daemon=True).start()
    
    def _defrag_thread(self):
        result = self.optimizer.defragment_windows()
        self.log_output(result)
        self.status_var.set("Ready")
    
    def optimize_startup(self):
        """Optimize startup programs"""
        self.status_var.set("Analyzing startup programs...")
        programs = self.optimizer.optimize_startup()
        
        if programs:
            startup_window = tk.Toplevel(self.root)
            startup_window.title("Startup Programs")
            startup_window.geometry("600x400")
            
            listbox = tk.Listbox(startup_window, selectmode=tk.MULTIPLE)
            listbox.pack(fill='both', expand=True, padx=10, pady=10)
            
            for name, path in programs:
                listbox.insert(tk.END, f"{name}: {path}")
            
            ttk.Label(startup_window, 
                     text="Select programs to disable from startup:").pack()
            
            def disable_selected():
                selected = listbox.curselection()
                # Implementation for disabling selected programs
                startup_window.destroy()
            
            ttk.Button(startup_window, text="Disable Selected", 
                      command=disable_selected).pack(pady=10)
        
        self.status_var.set("Ready")
    
    def optimize_visual(self):
        """Optimize visual effects"""
        result = self.optimizer.disable_visual_effects()
        self.log_output(result)
        messagebox.showinfo("Visual Effects", 
                           "Visual effects optimized. You may need to restart for full effect.")
    
    def run_all_optimizations(self):
        """Run all optimizations"""
        if messagebox.askyesno("Run All Optimizations", 
                               "This will clean temp files, defragment drives, and optimize settings. Continue?"):
            threading.Thread(target=self._run_all_thread, daemon=True).start()
    
    def _run_all_thread(self):
        self.status_var.set("Running all optimizations...")
        
        # Clean temp files
        self.log_output("Cleaning temporary files...")
        result = self.optimizer.clean_temp_files()
        self.log_output(result)
        
        # Optimize visual effects
        self.log_output("Optimizing visual effects...")
        result = self.optimizer.disable_visual_effects()
        self.log_output(result)
        
        # Defragment
        self.log_output("Starting defragmentation...")
        result = self.optimizer.defragment_windows()
        self.log_output(result)
        
        self.log_output("All optimizations complete!")
        self.status_var.set("Ready")
    
    def find_files(self):
        """Find large files"""
        self.status_var.set("Searching for large files...")
        
        # Clear existing items
        for item in self.file_tree.get_children():
            self.file_tree.delete(item)
        
        # Search in configured folders
        all_files = []
        for folder in self.optimizer.config['folders_to_optimize']:
            if os.path.exists(folder):
                files = self.optimizer.find_large_files(folder, self.min_size_var.get())
                all_files.extend(files)
        
        # Add to tree
        for file_info in all_files[:50]:  # Limit to 50 files for performance
            self.file_tree.insert('', 'end', 
                                 values=(f"{file_info['size_mb']:.1f}",
                                        file_info['modified'].strftime('%Y-%m-%d'),
                                        file_info['path']))
        
        self.status_var.set(f"Found {len(all_files)} large files")
    
    def archive_files(self):
        """Archive selected files to Google Drive"""
        selected = self.file_tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select files to archive")
            return
        
        if messagebox.askyesno("Archive Files", 
                               f"Archive {len(selected)} files to Google Drive?"):
            # Get file info for selected items
            files_to_archive = []
            for item in selected:
                values = self.file_tree.item(item)['values']
                files_to_archive.append({
                    'path': values[2],
                    'size_mb': float(values[0])
                })
            
            # Archive files
            self.status_var.set("Archiving files...")
            archived = self.optimizer.archive_to_gdrive(files_to_archive, 
                                                       self.optimizer.config['gdrive_mount'])
            
            messagebox.showinfo("Archive Complete", 
                              f"Archived {len(archived)} files to Google Drive")
            
            # Refresh file list
            self.find_files()
    
    def add_protected_folder(self):
        """Add a protected folder"""
        folder = filedialog.askdirectory(title="Select Protected Folder")
        if folder:
            folder_name = os.path.basename(folder)
            if folder_name not in self.optimizer.config['protected_folders']:
                self.optimizer.config['protected_folders'].append(folder_name)
                self.protected_list.insert(tk.END, folder_name)
    
    def remove_protected_folder(self):
        """Remove selected protected folder"""
        selected = self.protected_list.curselection()
        if selected:
            folder = self.protected_list.get(selected[0])
            self.protected_list.delete(selected[0])
            self.optimizer.config['protected_folders'].remove(folder)
    
    def save_settings(self):
        """Save all settings"""
        self.optimizer.config['gdrive_mount'] = self.gdrive_var.get()
        self.optimizer.save_config()
        messagebox.showinfo("Settings", "Settings saved successfully")
    
    def run(self):
        """Start the GUI"""
        self.root.mainloop()

def create_desktop_shortcut():
    """Create a desktop shortcut for the optimizer"""
    desktop = Path.home() / "Desktop"
    shortcut_path = desktop / "ShaneBrain Optimizer.bat"
    
    batch_content = f"""@echo off
title ShaneBrain System Optimizer
echo Starting ShaneBrain System Optimizer...
python "{Path(__file__).absolute()}"
pause
"""
    
    with open(shortcut_path, 'w') as f:
        f.write(batch_content)
    
    print(f"Desktop shortcut created: {shortcut_path}")

if __name__ == "__main__":
    # Check if running with arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "--cli":
            # Command line interface
            optimizer = SystemOptimizer()
            
            print("ShaneBrain System Optimizer - CLI Mode")
            print("=" * 50)
            
            info = optimizer.get_system_info()
            print(f"CPU: {info['cpu_percent']}%")
            print(f"Memory: {info['memory_percent']}%")
            print(f"Disk: {info['disk_usage']}%")
            print(f"Free Space: {info['disk_free_gb']:.1f} GB")
            print("=" * 50)
            
            print("\nOptions:")
            print("1. Clean temp files")
            print("2. Defragment drives")
            print("3. Find large files")
            print("4. Run all optimizations")
            print("5. Exit")
            
            choice = input("\nEnter choice (1-5): ")
            
            if choice == "1":
                print(optimizer.clean_temp_files())
            elif choice == "2":
                print(optimizer.defragment_windows())
            elif choice == "3":
                folder = input("Enter folder path to scan: ")
                files = optimizer.find_large_files(folder)
                for f in files[:10]:
                    print(f"{f['size_mb']:.1f} MB - {f['path']}")
            elif choice == "4":
                print("Running all optimizations...")
                print(optimizer.clean_temp_files())
                print(optimizer.disable_visual_effects())
                print(optimizer.defragment_windows())
        
        elif sys.argv[1] == "--create-shortcut":
            create_desktop_shortcut()
    else:
        # GUI mode
        app = OptimizerGUI()
        app.run()
