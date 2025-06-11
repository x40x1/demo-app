"""
Demo Mode Application - Main Entry Point
A retail demo application for showcasing PCs in stores like MediaMarkt.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import time
import os
import sys
from datetime import datetime
import json

from settings_manager import SettingsManager
from input_controller import InputController
from media_player import MediaPlayer
from app_launcher import AppLauncher
from system_utils import SystemUtils

class DemoModeApp:
    def __init__(self):
        self.root = tk.Tk()
        self.settings_manager = SettingsManager()
        self.input_controller = InputController(self)
        self.media_player = MediaPlayer(self)
        self.app_launcher = AppLauncher(self)
        self.system_utils = SystemUtils()
        
        # Application state
        self.is_demo_active = False
        self.is_fullscreen = False
        self.is_keyboard_locked = False
        self.last_activity_time = time.time()
        self.demo_content = []
        self.current_content_index = 0
        
        # Emergency escape combination: Ctrl+Alt+Shift+Esc
        self.escape_keys = {'ctrl', 'alt', 'shift', 'esc'}
        self.pressed_keys = set()
        
        self.setup_main_window()
        self.setup_ui()
        self.load_settings()
        
        # Start input monitoring
        self.input_controller.start_monitoring()
        
        # Check if should start in demo mode
        if self.settings_manager.get('auto_start_demo', False):
            self.root.after(2000, self.start_demo_mode)  # Start after 2 seconds
    
    def setup_main_window(self):
        """Initialize the main application window"""
        self.root.title("Demo Mode - Retail PC Showcase")
        self.root.geometry("800x600")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Hide window initially if auto-start is enabled
        if self.settings_manager.get('auto_start_demo', False):
            self.root.withdraw()
    
    def setup_ui(self):
        """Setup the main user interface"""
        # Create main container
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Demo Mode Application", 
                               font=('Arial', 18, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Status frame
        status_frame = ttk.LabelFrame(main_frame, text="Status", padding="10")
        status_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        status_frame.columnconfigure(1, weight=1)
        
        # Status indicators
        ttk.Label(status_frame, text="Demo Mode:").grid(row=0, column=0, sticky=tk.W)
        self.demo_status_label = ttk.Label(status_frame, text="Inactive", foreground="red")
        self.demo_status_label.grid(row=0, column=1, sticky=tk.W)
        
        ttk.Label(status_frame, text="Keyboard Lock:").grid(row=1, column=0, sticky=tk.W)
        self.keyboard_status_label = ttk.Label(status_frame, text="Unlocked", foreground="green")
        self.keyboard_status_label.grid(row=1, column=1, sticky=tk.W)
        
        ttk.Label(status_frame, text="Content Items:").grid(row=2, column=0, sticky=tk.W)
        self.content_count_label = ttk.Label(status_frame, text="0")
        self.content_count_label.grid(row=2, column=1, sticky=tk.W)
        
        # Control buttons frame
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=2, column=0, columnspan=2, pady=(0, 20))
        
        # Main control buttons
        self.start_demo_btn = ttk.Button(control_frame, text="Start Demo Mode", 
                                        command=self.start_demo_mode, style="Accent.TButton")
        self.start_demo_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.stop_demo_btn = ttk.Button(control_frame, text="Stop Demo Mode", 
                                       command=self.stop_demo_mode, state="disabled")
        self.stop_demo_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.settings_btn = ttk.Button(control_frame, text="Settings", 
                                      command=self.open_settings)
        self.settings_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Content management frame
        content_frame = ttk.LabelFrame(main_frame, text="Demo Content", padding="10")
        content_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 20))
        content_frame.columnconfigure(0, weight=1)
        content_frame.rowconfigure(1, weight=1)
        
        # Content buttons
        content_btn_frame = ttk.Frame(content_frame)
        content_btn_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Button(content_btn_frame, text="Add Photos", 
                  command=self.add_photos).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(content_btn_frame, text="Add Videos", 
                  command=self.add_videos).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(content_btn_frame, text="Add Application", 
                  command=self.add_application).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(content_btn_frame, text="Remove Selected", 
                  command=self.remove_content).pack(side=tk.RIGHT)
        
        # Content listbox
        listbox_frame = ttk.Frame(content_frame)
        listbox_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        listbox_frame.columnconfigure(0, weight=1)
        listbox_frame.rowconfigure(0, weight=1)
        
        self.content_listbox = tk.Listbox(listbox_frame)
        self.content_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollbar for listbox
        scrollbar = ttk.Scrollbar(listbox_frame, orient="vertical", command=self.content_listbox.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.content_listbox.configure(yscrollcommand=scrollbar.set)
        
        # Update content display
        self.update_content_display()
    
    def load_settings(self):
        """Load application settings"""
        # Update UI based on settings
        content = self.settings_manager.get('demo_content', [])
        self.demo_content = content
        self.update_content_display()
    
    def update_content_display(self):
        """Update the content listbox display"""
        self.content_listbox.delete(0, tk.END)
        for item in self.demo_content:
            display_text = f"{item['type'].upper()}: {os.path.basename(item['path'])}"
            if item['type'] == 'application':
                display_text += f" (Launch: {item.get('launch_mode', 'desktop')})"
            self.content_listbox.insert(tk.END, display_text)
        
        self.content_count_label.config(text=str(len(self.demo_content)))
    
    def add_photos(self):
        """Add photo files to demo content"""
        filetypes = [("Image files", "*.jpg *.jpeg *.png *.gif *.bmp")]
        files = filedialog.askopenfilenames(title="Select Photos", filetypes=filetypes)
        
        for file in files:
            content_item = {
                'type': 'photo',
                'path': file,
                'duration': self.settings_manager.get('photo_duration', 5)
            }
            self.demo_content.append(content_item)
        
        self.save_content()
        self.update_content_display()
    
    def add_videos(self):
        """Add video files to demo content"""
        filetypes = [("Video files", "*.mp4 *.avi *.mov *.wmv *.mkv")]
        files = filedialog.askopenfilenames(title="Select Videos", filetypes=filetypes)
        
        for file in files:
            content_item = {
                'type': 'video',
                'path': file
            }
            self.demo_content.append(content_item)
        
        self.save_content()
        self.update_content_display()
    
    def add_application(self):
        """Add application to demo content"""
        app_dialog = ApplicationDialog(self.root)
        self.root.wait_window(app_dialog.dialog)
        
        if app_dialog.result:
            self.demo_content.append(app_dialog.result)
            self.save_content()
            self.update_content_display()
    
    def remove_content(self):
        """Remove selected content item"""
        selection = self.content_listbox.curselection()
        if selection:
            index = selection[0]
            del self.demo_content[index]
            self.save_content()
            self.update_content_display()
    
    def save_content(self):
        """Save demo content to settings"""
        self.settings_manager.set('demo_content', self.demo_content)
    
    def start_demo_mode(self):
        """Start the demo mode"""
        if not self.demo_content:
            messagebox.showwarning("No Content", "Please add some content before starting demo mode.")
            return
        
        self.is_demo_active = True
        self.update_status_display()
        
        # Hide main window and show fullscreen demo
        self.root.withdraw()
        self.show_fullscreen_demo()
        
        # Apply keyboard lock if enabled
        if self.settings_manager.get('keyboard_lock_enabled', False):
            self.input_controller.lock_keyboard()
            self.is_keyboard_locked = True
    
    def stop_demo_mode(self):
        """Stop the demo mode"""
        self.is_demo_active = False
        self.is_fullscreen = False
        
        # Unlock keyboard
        if self.is_keyboard_locked:
            self.input_controller.unlock_keyboard()
            self.is_keyboard_locked = False
        
        # Hide fullscreen and show main window
        self.media_player.stop_playback()
        self.root.deiconify()
        self.update_status_display()
    
    def show_fullscreen_demo(self):
        """Show fullscreen demo content"""
        if not self.demo_content:
            return
        
        self.is_fullscreen = True
        self.current_content_index = 0
        self.play_current_content()
    
    def play_current_content(self):
        """Play the current content item"""
        if not self.is_demo_active or not self.demo_content:
            return
        
        content = self.demo_content[self.current_content_index]
        
        if content['type'] in ['photo', 'video']:
            self.media_player.play_content(content)
        elif content['type'] == 'application':
            self.app_launcher.launch_application(content)
        
        # Schedule next content
        self.schedule_next_content()
    
    def schedule_next_content(self):
        """Schedule the next content to play"""
        if not self.is_demo_active:
            return
        
        content = self.demo_content[self.current_content_index]
        duration = content.get('duration', 10)  # Default 10 seconds
        
        # Move to next content
        self.current_content_index = (self.current_content_index + 1) % len(self.demo_content)
        
        # Schedule next content
        threading.Timer(duration, self.play_current_content).start()
    
    def handle_escape_attempt(self):
        """Handle emergency escape key combination"""
        if not self.is_demo_active:
            return
        
        # Check if escape combination is pressed
        if self.escape_keys.issubset(self.pressed_keys):
            self.prompt_master_password()
    
    def prompt_master_password(self):
        """Prompt for master password to exit demo mode"""
        stored_password = self.settings_manager.get('master_password')

        # If no password is set, exit directly without prompting
        if not stored_password:
            self.stop_demo_mode()
            return

        password_dialog = PasswordDialog(
            self.root,
            "Enter Master Password",
            "Enter the master password to exit demo mode:"
        )
        self.root.wait_window(password_dialog.dialog)

        if password_dialog.result:
            if self.settings_manager.verify_password(password_dialog.result, stored_password):
                self.stop_demo_mode()
            else:
                messagebox.showerror("Access Denied", "Incorrect password.")
    
    def open_settings(self):
        """Open settings dialog"""
        # First verify master password
        stored_password = self.settings_manager.get('master_password')
        if stored_password:
            password_dialog = PasswordDialog(self.root, "Master Password Required", 
                                           "Enter the master password to access settings:")
            self.root.wait_window(password_dialog.dialog)
            
            if not password_dialog.result or not self.settings_manager.verify_password(
                password_dialog.result, stored_password):
                messagebox.showerror("Access Denied", "Incorrect password.")
                return
        
        # Open settings dialog
        settings_dialog = SettingsDialog(self.root, self.settings_manager)
        self.root.wait_window(settings_dialog.dialog)
    
    def update_status_display(self):
        """Update status indicators in UI"""
        if self.is_demo_active:
            self.demo_status_label.config(text="Active", foreground="green")
            self.start_demo_btn.config(state="disabled")
            self.stop_demo_btn.config(state="normal")
        else:
            self.demo_status_label.config(text="Inactive", foreground="red")
            self.start_demo_btn.config(state="normal")
            self.stop_demo_btn.config(state="disabled")
        
        if self.is_keyboard_locked:
            self.keyboard_status_label.config(text="Locked", foreground="red")
        else:
            self.keyboard_status_label.config(text="Unlocked", foreground="green")
    
    def on_activity_detected(self):
        """Called when user activity is detected"""
        self.last_activity_time = time.time()
        
        if self.is_demo_active and self.is_fullscreen:
            # Hide demo and show main window
            self.media_player.hide_fullscreen()
            self.root.deiconify()
            self.is_fullscreen = False
            
            # Schedule return to fullscreen after inactivity
            self.schedule_inactivity_check()
    
    def schedule_inactivity_check(self):
        """Schedule check for returning to fullscreen after inactivity"""
        if not self.is_demo_active or self.is_fullscreen:
            return
        
        inactivity_timeout = self.settings_manager.get('inactivity_timeout', 30)  # seconds
        
        def check_inactivity():
            if self.is_demo_active and not self.is_fullscreen:
                time_since_activity = time.time() - self.last_activity_time
                if time_since_activity >= inactivity_timeout:
                    self.root.withdraw()
                    self.is_fullscreen = True
                    self.media_player.show_fullscreen()
                else:
                    # Check again in 1 second
                    threading.Timer(1, check_inactivity).start()
        
        threading.Timer(1, check_inactivity).start()
    
    def on_closing(self):
        """Handle application closing"""
        if self.is_demo_active:
            result = messagebox.askyesno("Demo Running", 
                                       "Demo mode is active. Stop demo and exit?")
            if result:
                self.stop_demo_mode()
            else:
                return
        
        # Stop input monitoring
        self.input_controller.stop_monitoring()
        
        # Clean up and exit
        self.root.destroy()
    
    def run(self):
        """Start the application"""
        self.root.mainloop()


class ApplicationDialog:
    """Dialog for adding applications to demo content"""
    def __init__(self, parent):
        self.result = None
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Add Application")
        self.dialog.geometry("500x300")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center dialog
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (300 // 2)
        self.dialog.geometry(f"500x300+{x}+{y}")
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup dialog UI"""
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Application name
        ttk.Label(main_frame, text="Application Name:").pack(anchor=tk.W)
        self.name_entry = ttk.Entry(main_frame, width=50)
        self.name_entry.pack(fill=tk.X, pady=(0, 10))
        
        # Application path
        ttk.Label(main_frame, text="Application Path:").pack(anchor=tk.W)
        path_frame = ttk.Frame(main_frame)
        path_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.path_entry = ttk.Entry(path_frame)
        self.path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        ttk.Button(path_frame, text="Browse", 
                  command=self.browse_application).pack(side=tk.RIGHT, padx=(10, 0))
        
        # Launch mode
        ttk.Label(main_frame, text="Launch Mode:").pack(anchor=tk.W)
        self.launch_mode = tk.StringVar(value="desktop")
        
        mode_frame = ttk.Frame(main_frame)
        mode_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Radiobutton(mode_frame, text="Desktop Application", 
                       variable=self.launch_mode, value="desktop").pack(anchor=tk.W)
        ttk.Radiobutton(mode_frame, text="Web URL", 
                       variable=self.launch_mode, value="web").pack(anchor=tk.W)
        
        # Duration
        ttk.Label(main_frame, text="Display Duration (seconds):").pack(anchor=tk.W)
        self.duration_var = tk.StringVar(value="30")
        duration_spinbox = ttk.Spinbox(main_frame, from_=5, to=300, 
                                      textvariable=self.duration_var, width=10)
        duration_spinbox.pack(anchor=tk.W, pady=(0, 20))
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        ttk.Button(button_frame, text="Cancel", 
                  command=self.cancel).pack(side=tk.RIGHT, padx=(10, 0))
        ttk.Button(button_frame, text="Add", 
                  command=self.add_application).pack(side=tk.RIGHT)
    
    def browse_application(self):
        """Browse for application executable"""
        if self.launch_mode.get() == "desktop":
            filetypes = [("Executable files", "*.exe"), ("All files", "*.*")]
            filename = filedialog.askopenfilename(title="Select Application", filetypes=filetypes)
        else:
            filename = tk.simpledialog.askstring("Web URL", "Enter web URL:")
        
        if filename:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, filename)
    
    def add_application(self):
        """Add application to demo content"""
        name = self.name_entry.get().strip()
        path = self.path_entry.get().strip()
        
        if not name or not path:
            messagebox.showerror("Error", "Please fill in all fields.")
            return
        
        try:
            duration = int(self.duration_var.get())
        except ValueError:
            messagebox.showerror("Error", "Duration must be a number.")
            return
        
        self.result = {
            'type': 'application',
            'name': name,
            'path': path,
            'launch_mode': self.launch_mode.get(),
            'duration': duration
        }
        
        self.dialog.destroy()
    
    def cancel(self):
        """Cancel dialog"""
        self.dialog.destroy()


class PasswordDialog:
    """Dialog for password input"""
    def __init__(self, parent, title, message):
        self.result = None
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("400x150")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center dialog
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (150 // 2)
        self.dialog.geometry(f"400x150+{x}+{y}")
        
        self.setup_ui(message)
    
    def setup_ui(self, message):
        """Setup dialog UI"""
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text=message).pack(pady=(0, 10))
        
        self.password_entry = ttk.Entry(main_frame, show="*", width=30)
        self.password_entry.pack(pady=(0, 20))
        self.password_entry.focus()
        self.password_entry.bind('<Return>', lambda e: self.ok())
        
        button_frame = ttk.Frame(main_frame)
        button_frame.pack()
        
        ttk.Button(button_frame, text="Cancel", 
                  command=self.cancel).pack(side=tk.RIGHT, padx=(10, 0))
        ttk.Button(button_frame, text="OK", 
                  command=self.ok).pack(side=tk.RIGHT)
    
    def ok(self):
        """OK button clicked"""
        self.result = self.password_entry.get()
        self.dialog.destroy()
    
    def cancel(self):
        """Cancel button clicked"""
        self.dialog.destroy()


class SettingsDialog:
    """Settings configuration dialog"""
    def __init__(self, parent, settings_manager):
        self.settings_manager = settings_manager
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Demo Mode Settings")
        self.dialog.geometry("600x500")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center dialog
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (600 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (500 // 2)
        self.dialog.geometry(f"600x500+{x}+{y}")
        
        self.setup_ui()
        self.load_current_settings()
    
    def setup_ui(self):
        """Setup settings UI"""
        # Create notebook for tabs
        notebook = ttk.Notebook(self.dialog)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # General settings tab
        general_frame = ttk.Frame(notebook)
        notebook.add(general_frame, text="General")
        
        self.setup_general_tab(general_frame)
        
        # Security settings tab
        security_frame = ttk.Frame(notebook)
        notebook.add(security_frame, text="Security")
        
        self.setup_security_tab(security_frame)
        
        # Timing settings tab
        timing_frame = ttk.Frame(notebook)
        notebook.add(timing_frame, text="Timing")
        
        self.setup_timing_tab(timing_frame)
        
        # Startup settings tab
        startup_frame = ttk.Frame(notebook)
        notebook.add(startup_frame, text="Startup")
        
        self.setup_startup_tab(startup_frame)
        
        # Buttons
        button_frame = ttk.Frame(self.dialog)
        button_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        ttk.Button(button_frame, text="Cancel", 
                  command=self.cancel).pack(side=tk.RIGHT, padx=(10, 0))
        ttk.Button(button_frame, text="Save", 
                  command=self.save_settings).pack(side=tk.RIGHT)
    
    def setup_general_tab(self, parent):
        """Setup general settings tab"""
        frame = ttk.Frame(parent, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Auto-start demo
        self.auto_start_var = tk.BooleanVar()
        ttk.Checkbutton(frame, text="Auto-start demo mode on application launch", 
                       variable=self.auto_start_var).pack(anchor=tk.W, pady=(0, 10))
        
        # Default photo duration
        ttk.Label(frame, text="Default photo display duration (seconds):").pack(anchor=tk.W)
        self.photo_duration_var = tk.StringVar()
        ttk.Spinbox(frame, from_=1, to=60, textvariable=self.photo_duration_var, 
                   width=10).pack(anchor=tk.W, pady=(0, 10))
    
    def setup_security_tab(self, parent):
        """Setup security settings tab"""
        frame = ttk.Frame(parent, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Master password
        ttk.Label(frame, text="Master Password:").pack(anchor=tk.W)
        self.master_password_entry = ttk.Entry(frame, show="*", width=30)
        self.master_password_entry.pack(anchor=tk.W, pady=(0, 10))
        
        # Confirm password
        ttk.Label(frame, text="Confirm Password:").pack(anchor=tk.W)
        self.confirm_password_entry = ttk.Entry(frame, show="*", width=30)
        self.confirm_password_entry.pack(anchor=tk.W, pady=(0, 10))
        
        # Keyboard lock
        self.keyboard_lock_var = tk.BooleanVar()
        ttk.Checkbutton(frame, text="Enable complete keyboard lock (requires admin privileges)", 
                       variable=self.keyboard_lock_var).pack(anchor=tk.W, pady=(0, 10))
        
        ttk.Label(frame, text="Note: Emergency exit combination is Ctrl+Alt+Shift+Esc", 
                 font=('Arial', 9, 'italic')).pack(anchor=tk.W)
    
    def setup_timing_tab(self, parent):
        """Setup timing settings tab"""
        frame = ttk.Frame(parent, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Inactivity timeout
        ttk.Label(frame, text="Return to fullscreen after inactivity (seconds):").pack(anchor=tk.W)
        self.inactivity_timeout_var = tk.StringVar()
        ttk.Spinbox(frame, from_=5, to=300, textvariable=self.inactivity_timeout_var, 
                   width=10).pack(anchor=tk.W, pady=(0, 10))
    
    def setup_startup_tab(self, parent):
        """Setup startup settings tab"""
        frame = ttk.Frame(parent, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Auto-start with Windows
        self.windows_startup_var = tk.BooleanVar()
        ttk.Checkbutton(frame, text="Start with Windows (auto-start on boot)", 
                       variable=self.windows_startup_var).pack(anchor=tk.W, pady=(0, 10))
        
        ttk.Label(frame, text="Note: This will add the application to Windows startup programs", 
                 font=('Arial', 9, 'italic')).pack(anchor=tk.W)
    
    def load_current_settings(self):
        """Load current settings into UI"""
        self.auto_start_var.set(self.settings_manager.get('auto_start_demo', False))
        self.photo_duration_var.set(str(self.settings_manager.get('photo_duration', 5)))
        self.keyboard_lock_var.set(self.settings_manager.get('keyboard_lock_enabled', False))
        self.inactivity_timeout_var.set(str(self.settings_manager.get('inactivity_timeout', 30)))
        self.windows_startup_var.set(self.settings_manager.get('windows_startup', False))
    
    def save_settings(self):
        """Save settings"""
        # Validate password if provided
        password = self.master_password_entry.get()
        confirm = self.confirm_password_entry.get()
        
        if password or confirm:
            if password != confirm:
                messagebox.showerror("Error", "Passwords do not match.")
                return
            
            if len(password) < 4:
                messagebox.showerror("Error", "Password must be at least 4 characters.")
                return
            
            # Hash and save password
            hashed_password = self.settings_manager.hash_password(password)
            self.settings_manager.set('master_password', hashed_password)
        
        # Save other settings
        try:
            self.settings_manager.set('auto_start_demo', self.auto_start_var.get())
            self.settings_manager.set('photo_duration', int(self.photo_duration_var.get()))
            self.settings_manager.set('keyboard_lock_enabled', self.keyboard_lock_var.get())
            self.settings_manager.set('inactivity_timeout', int(self.inactivity_timeout_var.get()))
            self.settings_manager.set('windows_startup', self.windows_startup_var.get())
            
            messagebox.showinfo("Success", "Settings saved successfully.")
            self.dialog.destroy()
            
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid value: {e}")
    
    def cancel(self):
        """Cancel settings dialog"""
        self.dialog.destroy()


if __name__ == "__main__":
    app = DemoModeApp()
    app.run()
