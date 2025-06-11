"""
Media Player - Handles photo and video playback in fullscreen mode
"""

import tkinter as tk
from tkinter import ttk
import pygame
import cv2
import threading
import time
import os
from PIL import Image, ImageTk
import numpy as np

class MediaPlayer:
    def __init__(self, app):
        self.app = app
        self.current_content = None
        self.fullscreen_window = None
        self.is_playing = False
        self.video_thread = None
        
        # Initialize pygame for audio/video
        pygame.mixer.init()
        
        # Video playback variables
        self.video_cap = None
        self.video_fps = 30
        self.frame_delay = 1.0 / self.video_fps
    
    def play_content(self, content):
        """Play media content (photo or video)"""
        self.current_content = content
        
        if content['type'] == 'photo':
            self.play_photo(content)
        elif content['type'] == 'video':
            self.play_video(content)
    
    def play_photo(self, content):
        """Display a photo in fullscreen"""
        try:
            # Load and display image
            image_path = content['path']
            if not os.path.exists(image_path):
                print(f"Image file not found: {image_path}")
                return
            
            # Create fullscreen window if not exists
            if not self.fullscreen_window:
                self.create_fullscreen_window()
            
            # Load and resize image to fit screen
            pil_image = Image.open(image_path)
            screen_width = self.fullscreen_window.winfo_screenwidth()
            screen_height = self.fullscreen_window.winfo_screenheight()
            
            # Calculate scaling to fit screen while maintaining aspect ratio
            img_width, img_height = pil_image.size
            scale_x = screen_width / img_width
            scale_y = screen_height / img_height
            scale = min(scale_x, scale_y)
            
            new_width = int(img_width * scale)
            new_height = int(img_height * scale)
            
            pil_image = pil_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Convert to tkinter format
            tk_image = ImageTk.PhotoImage(pil_image)
            
            # Display image
            if hasattr(self, 'image_label'):
                self.image_label.destroy()
            
            self.image_label = tk.Label(self.fullscreen_window, image=tk_image, bg='black')
            self.image_label.image = tk_image  # Keep a reference
            self.image_label.pack(expand=True)
            
            self.is_playing = True
            self.fullscreen_window.deiconify()
            self.fullscreen_window.lift()
            self.fullscreen_window.focus_force()
            
        except Exception as e:
            print(f"Error playing photo: {e}")
    
    def play_video(self, content):
        """Play a video in fullscreen"""
        try:
            video_path = content['path']
            if not os.path.exists(video_path):
                print(f"Video file not found: {video_path}")
                return
            
            # Create fullscreen window if not exists
            if not self.fullscreen_window:
                self.create_fullscreen_window()
            
            # Open video with OpenCV
            self.video_cap = cv2.VideoCapture(video_path)
            if not self.video_cap.isOpened():
                print(f"Could not open video: {video_path}")
                return
            
            # Get video properties
            self.video_fps = self.video_cap.get(cv2.CAP_PROP_FPS) or 30
            self.frame_delay = 1.0 / self.video_fps
            
            # Create video label
            if hasattr(self, 'video_label'):
                self.video_label.destroy()
            
            self.video_label = tk.Label(self.fullscreen_window, bg='black')
            self.video_label.pack(expand=True, fill=tk.BOTH)
            
            self.is_playing = True
            self.fullscreen_window.deiconify()
            self.fullscreen_window.lift()
            self.fullscreen_window.focus_force()
            
            # Start video playback thread
            self.video_thread = threading.Thread(target=self._video_playback_loop, daemon=True)
            self.video_thread.start()
            
        except Exception as e:
            print(f"Error playing video: {e}")
    
    def _video_playback_loop(self):
        """Video playback loop running in separate thread"""
        screen_width = self.fullscreen_window.winfo_screenwidth()
        screen_height = self.fullscreen_window.winfo_screenheight()
        
        while self.is_playing and self.video_cap and self.video_cap.isOpened():
            ret, frame = self.video_cap.read()
            
            if not ret:
                # Loop video
                self.video_cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue
            
            try:
                # Resize frame to fit screen
                frame_height, frame_width = frame.shape[:2]
                scale_x = screen_width / frame_width
                scale_y = screen_height / frame_height
                scale = min(scale_x, scale_y)
                
                new_width = int(frame_width * scale)
                new_height = int(frame_height * scale)
                
                frame = cv2.resize(frame, (new_width, new_height))
                
                # Convert BGR to RGB
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                # Convert to PIL Image and then to tkinter
                pil_image = Image.fromarray(frame)
                tk_image = ImageTk.PhotoImage(pil_image)
                
                # Update video label on main thread
                if self.video_label and self.is_playing:
                    self.fullscreen_window.after(0, self._update_video_frame, tk_image)
                
                time.sleep(self.frame_delay)
                
            except Exception as e:
                print(f"Error in video playback: {e}")
                break
        
        # Clean up
        if self.video_cap:
            self.video_cap.release()
            self.video_cap = None
    
    def _update_video_frame(self, tk_image):
        """Update video frame on main thread"""
        if self.video_label and self.is_playing:
            self.video_label.configure(image=tk_image)
            self.video_label.image = tk_image  # Keep reference
    
    def create_fullscreen_window(self):
        """Create fullscreen window for media display"""
        self.fullscreen_window = tk.Toplevel()
        self.fullscreen_window.title("Demo Content")
        self.fullscreen_window.configure(bg='black')
        
        # Make fullscreen
        self.fullscreen_window.attributes('-fullscreen', True)
        self.fullscreen_window.attributes('-topmost', True)
        self.fullscreen_window.overrideredirect(True)
        
        # Hide initially
        self.fullscreen_window.withdraw()
        
        # Bind escape key (in case keyboard isn't locked)
        self.fullscreen_window.bind('<KeyPress>', self._on_key_press)
        self.fullscreen_window.focus_set()
    
    def _on_key_press(self, event):
        """Handle key press in fullscreen window"""
        # Let the main app handle escape combination
        if hasattr(self.app, 'input_controller'):
            # Key press detected - activity
            self.app.on_activity_detected()
    
    def show_fullscreen(self):
        """Show fullscreen window"""
        if self.fullscreen_window:
            self.fullscreen_window.deiconify()
            self.fullscreen_window.lift()
            self.fullscreen_window.focus_force()
    
    def hide_fullscreen(self):
        """Hide fullscreen window"""
        if self.fullscreen_window:
            self.fullscreen_window.withdraw()
    
    def stop_playback(self):
        """Stop current media playback"""
        self.is_playing = False
        
        # Stop video
        if self.video_cap:
            self.video_cap.release()
            self.video_cap = None
        
        # Hide fullscreen window
        if self.fullscreen_window:
            self.fullscreen_window.withdraw()
    
    def cleanup(self):
        """Cleanup resources"""
        self.stop_playback()
        
        if self.fullscreen_window:
            self.fullscreen_window.destroy()
            self.fullscreen_window = None
        
        pygame.mixer.quit()


class SimpleImageViewer:
    """Simple image viewer for systems without full multimedia support"""
    def __init__(self, app):
        self.app = app
        self.fullscreen_window = None
        self.current_image = None
    
    def show_image(self, image_path, duration=5):
        """Show image for specified duration"""
        try:
            if not self.fullscreen_window:
                self.create_fullscreen_window()
            
            # Load and display image
            pil_image = Image.open(image_path)
            
            # Get screen dimensions
            screen_width = self.fullscreen_window.winfo_screenwidth()
            screen_height = self.fullscreen_window.winfo_screenheight()
            
            # Resize image to fit screen
            img_width, img_height = pil_image.size
            scale_x = screen_width / img_width
            scale_y = screen_height / img_height
            scale = min(scale_x, scale_y)
            
            new_width = int(img_width * scale)
            new_height = int(img_height * scale)
            
            pil_image = pil_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            tk_image = ImageTk.PhotoImage(pil_image)
            
            # Display image
            if hasattr(self, 'image_label'):
                self.image_label.destroy()
            
            self.image_label = tk.Label(self.fullscreen_window, image=tk_image, bg='black')
            self.image_label.image = tk_image
            self.image_label.pack(expand=True)
            
            self.fullscreen_window.deiconify()
            self.fullscreen_window.lift()
            
        except Exception as e:
            print(f"Error displaying image: {e}")
    
    def create_fullscreen_window(self):
        """Create simple fullscreen window"""
        self.fullscreen_window = tk.Toplevel()
        self.fullscreen_window.title("Demo Image")
        self.fullscreen_window.configure(bg='black')
        self.fullscreen_window.attributes('-fullscreen', True)
        self.fullscreen_window.withdraw()
    
    def hide(self):
        """Hide the image viewer"""
        if self.fullscreen_window:
            self.fullscreen_window.withdraw()
