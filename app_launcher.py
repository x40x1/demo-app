"""
Application Launcher - Handles launching external applications and web content
"""

import subprocess
import webbrowser
import os
import threading
import time
import psutil
import tkinter as tk
from tkinter import messagebox

class AppLauncher:
    def __init__(self, app):
        self.app = app
        self.running_processes = []
        self.browser_windows = []
    
    def launch_application(self, content):
        """Launch an application based on content configuration"""
        try:
            if content['launch_mode'] == 'desktop':
                self.launch_desktop_app(content)
            elif content['launch_mode'] == 'web':
                self.launch_web_content(content)
        except Exception as e:
            print(f"Error launching application: {e}")
    
    def launch_desktop_app(self, content):
        """Launch a desktop application"""
        app_path = content['path']
        app_name = content.get('name', 'Application')
        
        try:
            if not os.path.exists(app_path):
                print(f"Application not found: {app_path}")
                return
            
            # Launch application
            process = subprocess.Popen([app_path], 
                                     stdout=subprocess.PIPE, 
                                     stderr=subprocess.PIPE)
            
            self.running_processes.append({
                'process': process,
                'name': app_name,
                'path': app_path,
                'start_time': time.time()
            })
            
            print(f"Launched application: {app_name}")
            
            # Monitor application in separate thread
            monitor_thread = threading.Thread(
                target=self._monitor_desktop_app, 
                args=(process, content), 
                daemon=True
            )
            monitor_thread.start()
            
        except Exception as e:
            print(f"Error launching desktop app {app_name}: {e}")
    
    def launch_web_content(self, content):
        """Launch web content in browser"""
        url = content['path']
        
        try:
            # Open in default browser
            webbrowser.open(url, new=2)  # new=2 opens in new tab if possible
            
            self.browser_windows.append({
                'url': url,
                'name': content.get('name', 'Web Content'),
                'start_time': time.time()
            })
            
            print(f"Opened web content: {url}")
            
            # Schedule closing after duration
            duration = content.get('duration', 30)
            close_timer = threading.Timer(duration, self._close_web_content, args=(url,))
            close_timer.start()
            
        except Exception as e:
            print(f"Error launching web content: {e}")
    
    def _monitor_desktop_app(self, process, content):
        """Monitor desktop application and close after duration"""
        duration = content.get('duration', 30)
        start_time = time.time()
        
        while time.time() - start_time < duration:
            if process.poll() is not None:
                # Process has ended
                break
            time.sleep(1)
        
        # Close application if still running
        try:
            if process.poll() is None:
                # Try graceful termination first
                process.terminate()
                
                # Wait a bit for graceful shutdown
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    # Force kill if still running
                    process.kill()
                    
                print(f"Closed application: {content.get('name', 'Unknown')}")
        except Exception as e:
            print(f"Error closing application: {e}")
        
        # Remove from running processes
        self.running_processes = [p for p in self.running_processes if p['process'] != process]
    
    def _close_web_content(self, url):
        """Close web content (attempt to close browser tabs)"""
        # Note: Closing specific browser tabs programmatically is limited
        # This is a best-effort approach
        print(f"Web content duration expired: {url}")
        
        # Remove from browser windows list
        self.browser_windows = [w for w in self.browser_windows if w['url'] != url]
    
    def close_all_applications(self):
        """Close all launched applications"""
        # Close desktop applications
        for app_info in self.running_processes:
            try:
                process = app_info['process']
                if process.poll() is None:
                    process.terminate()
                    try:
                        process.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        process.kill()
                print(f"Closed application: {app_info['name']}")
            except Exception as e:
                print(f"Error closing application {app_info['name']}: {e}")
        
        self.running_processes.clear()
        
        # Note: Browser windows are harder to close programmatically
        # Clear the tracking list
        self.browser_windows.clear()
    
    def get_running_applications(self):
        """Get list of currently running launched applications"""
        # Clean up finished processes
        active_processes = []
        for app_info in self.running_processes:
            if app_info['process'].poll() is None:
                active_processes.append(app_info)
        
        self.running_processes = active_processes
        return self.running_processes
    
    def force_close_application(self, app_name):
        """Force close a specific application by name"""
        for app_info in self.running_processes:
            if app_info['name'] == app_name:
                try:
                    process = app_info['process']
                    if process.poll() is None:
                        process.kill()
                    print(f"Force closed application: {app_name}")
                    self.running_processes.remove(app_info)
                    return True
                except Exception as e:
                    print(f"Error force closing {app_name}: {e}")
        return False


class KioskBrowser:
    """Specialized browser launcher for kiosk mode web content"""
    def __init__(self):
        self.browser_process = None
    
    def launch_kiosk_browser(self, url, duration=30):
        """Launch browser in kiosk mode"""
        try:
            # Try Chrome first (most common in retail environments)
            chrome_paths = [
                r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            ]
            
            chrome_path = None
            for path in chrome_paths:
                if os.path.exists(path):
                    chrome_path = path
                    break
            
            if chrome_path:
                # Launch Chrome in kiosk mode
                cmd = [chrome_path, "--kiosk", "--disable-infobars", 
                       "--disable-extensions", "--disable-plugins", url]
                self.browser_process = subprocess.Popen(cmd)
                
                # Schedule closing
                close_timer = threading.Timer(duration, self.close_browser)
                close_timer.start()
                
                return True
            else:
                # Fallback to default browser
                webbrowser.open(url, new=2)
                return True
                
        except Exception as e:
            print(f"Error launching kiosk browser: {e}")
            return False
    
    def close_browser(self):
        """Close kiosk browser"""
        if self.browser_process:
            try:
                self.browser_process.terminate()
                self.browser_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.browser_process.kill()
            except Exception as e:
                print(f"Error closing browser: {e}")
            finally:
                self.browser_process = None


class ApplicationMonitor:
    """Monitor and manage all launched applications"""
    def __init__(self, app_launcher):
        self.app_launcher = app_launcher
        self.monitoring = False
        self.monitor_thread = None
    
    def start_monitoring(self):
        """Start monitoring launched applications"""
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
    
    def stop_monitoring(self):
        """Stop monitoring"""
        self.monitoring = False
    
    def _monitor_loop(self):
        """Monitor loop to track application status"""
        while self.monitoring:
            try:
                # Update running applications list
                self.app_launcher.get_running_applications()
                
                # Monitor system resources
                cpu_percent = psutil.cpu_percent(interval=1)
                memory_percent = psutil.virtual_memory().percent
                
                # Log high resource usage
                if cpu_percent > 80 or memory_percent > 90:
                    print(f"High resource usage - CPU: {cpu_percent}%, Memory: {memory_percent}%")
                
                time.sleep(5)  # Check every 5 seconds
                
            except Exception as e:
                print(f"Error in application monitoring: {e}")
                time.sleep(10)
