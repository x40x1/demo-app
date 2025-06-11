"""
System Utilities - Windows system integration features
"""

import os
import sys
import winreg
import ctypes
from ctypes import wintypes
import subprocess
import shutil

class SystemUtils:
    def __init__(self):
        self.app_name = "DemoModeApp"
        self.startup_key = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
    
    def is_admin(self):
        """Check if running with administrator privileges"""
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    
    def request_admin_privileges(self):
        """Request administrator privileges (restart as admin)"""
        if self.is_admin():
            return True
        
        try:
            # Re-run the program with admin rights
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, " ".join(sys.argv), None, 1)
            return True
        except:
            return False
    
    def add_to_startup(self, app_path=None):
        """Add application to Windows startup"""
        if not app_path:
            app_path = sys.executable
        
        try:
            # Open registry key
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, self.startup_key, 0, winreg.KEY_SET_VALUE)
            
            # Set the value
            winreg.SetValueEx(key, self.app_name, 0, winreg.REG_SZ, f'"{app_path}"')
            
            # Close the key
            winreg.CloseKey(key)
            
            print(f"Added {self.app_name} to Windows startup")
            return True
            
        except Exception as e:
            print(f"Error adding to startup: {e}")
            return False
    
    def remove_from_startup(self):
        """Remove application from Windows startup"""
        try:
            # Open registry key
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, self.startup_key, 0, winreg.KEY_SET_VALUE)
            
            # Delete the value
            winreg.DeleteValue(key, self.app_name)
            
            # Close the key
            winreg.CloseKey(key)
            
            print(f"Removed {self.app_name} from Windows startup")
            return True
            
        except FileNotFoundError:
            # Value doesn't exist
            return True
        except Exception as e:
            print(f"Error removing from startup: {e}")
            return False
    
    def is_in_startup(self):
        """Check if application is in Windows startup"""
        try:
            # Open registry key
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, self.startup_key, 0, winreg.KEY_READ)
            
            # Try to read the value
            value, _ = winreg.QueryValueEx(key, self.app_name)
            
            # Close the key
            winreg.CloseKey(key)
            
            return True
            
        except FileNotFoundError:
            return False
        except Exception as e:
            print(f"Error checking startup: {e}")
            return False
    
    def create_desktop_shortcut(self, app_path=None, shortcut_name=None):
        """Create desktop shortcut"""
        if not app_path:
            app_path = sys.executable
        
        if not shortcut_name:
            shortcut_name = f"{self.app_name}.lnk"
        
        try:
            import win32com.client
            
            desktop = os.path.join(os.path.expanduser("~"), "Desktop")
            shortcut_path = os.path.join(desktop, shortcut_name)
            
            shell = win32com.client.Dispatch("WScript.Shell")
            shortcut = shell.CreateShortCut(shortcut_path)
            shortcut.Targetpath = app_path
            shortcut.WorkingDirectory = os.path.dirname(app_path)
            shortcut.IconLocation = app_path
            shortcut.save()
            
            print(f"Created desktop shortcut: {shortcut_path}")
            return True
            
        except Exception as e:
            print(f"Error creating desktop shortcut: {e}")
            return False
    
    def get_system_info(self):
        """Get system information"""
        try:
            info = {
                'platform': sys.platform,
                'python_version': sys.version,
                'is_admin': self.is_admin(),
                'executable_path': sys.executable,
                'script_path': os.path.abspath(__file__),
                'working_directory': os.getcwd()
            }
            
            # Get Windows version
            try:
                import platform
                info['windows_version'] = platform.platform()
                info['processor'] = platform.processor()
                info['architecture'] = platform.architecture()[0]
            except:
                pass
            
            return info
            
        except Exception as e:
            print(f"Error getting system info: {e}")
            return {}
    
    def create_executable(self, output_dir="dist"):
        """Create standalone executable using PyInstaller"""
        try:
            # Check if PyInstaller is available
            try:
                import PyInstaller
            except ImportError:
                print("PyInstaller not installed. Install with: pip install pyinstaller")
                return False
            
            # Get current script path
            script_path = os.path.abspath("demo_app.py")
            
            if not os.path.exists(script_path):
                print(f"Script not found: {script_path}")
                return False
            
            # Create PyInstaller command
            cmd = [
                "pyinstaller",
                "--onefile",  # Create single executable
                "--windowed",  # No console window
                "--name", self.app_name,
                "--distpath", output_dir,
                script_path
            ]
            
            # Run PyInstaller
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                exe_path = os.path.join(output_dir, f"{self.app_name}.exe")
                print(f"Executable created successfully: {exe_path}")
                return exe_path
            else:
                print(f"PyInstaller error: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"Error creating executable: {e}")
            return False
    
    def disable_task_manager(self):
        """Disable Task Manager (requires admin privileges)"""
        if not self.is_admin():
            print("Admin privileges required to disable Task Manager")
            return False
        
        try:
            # Registry path for Task Manager policy
            policy_key = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System"
            
            # Open registry key
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, policy_key, 0, 
                               winreg.KEY_SET_VALUE | winreg.KEY_CREATE_SUB_KEY)
            
            # Set DisableTaskMgr to 1
            winreg.SetValueEx(key, "DisableTaskMgr", 0, winreg.REG_DWORD, 1)
            
            # Close the key
            winreg.CloseKey(key)
            
            print("Task Manager disabled")
            return True
            
        except Exception as e:
            print(f"Error disabling Task Manager: {e}")
            return False
    
    def enable_task_manager(self):
        """Enable Task Manager"""
        try:
            # Registry path for Task Manager policy
            policy_key = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System"
            
            # Open registry key
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, policy_key, 0, winreg.KEY_SET_VALUE)
            
            # Delete DisableTaskMgr value or set to 0
            try:
                winreg.DeleteValue(key, "DisableTaskMgr")
            except FileNotFoundError:
                # Value doesn't exist, that's fine
                pass
            
            # Close the key
            winreg.CloseKey(key)
            
            print("Task Manager enabled")
            return True
            
        except Exception as e:
            print(f"Error enabling Task Manager: {e}")
            return False
    
    def lock_screen_saver(self):
        """Disable screen saver and power management"""
        try:
            # Disable screen saver
            subprocess.run(["powercfg", "/change", "standby-timeout-ac", "0"], check=True)
            subprocess.run(["powercfg", "/change", "standby-timeout-dc", "0"], check=True)
            subprocess.run(["powercfg", "/change", "monitor-timeout-ac", "0"], check=True)
            subprocess.run(["powercfg", "/change", "monitor-timeout-dc", "0"], check=True)
            
            print("Screen saver and power management disabled")
            return True
            
        except Exception as e:
            print(f"Error configuring power settings: {e}")
            return False
    
    def restore_power_settings(self):
        """Restore default power settings"""
        try:
            # Restore to balanced power plan defaults
            subprocess.run(["powercfg", "/restoredefaultschemes"], check=True)
            
            print("Power settings restored to defaults")
            return True
            
        except Exception as e:
            print(f"Error restoring power settings: {e}")
            return False


class WindowManager:
    """Manage window states and behaviors"""
    def __init__(self):
        self.user32 = ctypes.windll.user32
        self.kernel32 = ctypes.windll.kernel32
    
    def get_window_by_title(self, title):
        """Find window by title"""
        hwnd = self.user32.FindWindowW(None, title)
        return hwnd if hwnd else None
    
    def set_window_fullscreen(self, hwnd):
        """Set window to fullscreen"""
        if not hwnd:
            return False
        
        try:
            # Get screen dimensions
            screen_width = self.user32.GetSystemMetrics(0)
            screen_height = self.user32.GetSystemMetrics(1)
            
            # Set window style
            self.user32.SetWindowLongW(hwnd, -16, 0x80000000)  # WS_POPUP
            
            # Set window position and size
            self.user32.SetWindowPos(hwnd, -1, 0, 0, screen_width, screen_height, 0x0040)
            
            return True
            
        except Exception as e:
            print(f"Error setting fullscreen: {e}")
            return False
    
    def hide_taskbar(self):
        """Hide Windows taskbar"""
        try:
            taskbar = self.user32.FindWindowW("Shell_TrayWnd", None)
            if taskbar:
                self.user32.ShowWindow(taskbar, 0)  # SW_HIDE
                return True
            return False
        except Exception as e:
            print(f"Error hiding taskbar: {e}")
            return False
    
    def show_taskbar(self):
        """Show Windows taskbar"""
        try:
            taskbar = self.user32.FindWindowW("Shell_TrayWnd", None)
            if taskbar:
                self.user32.ShowWindow(taskbar, 1)  # SW_SHOW
                return True
            return False
        except Exception as e:
            print(f"Error showing taskbar: {e}")
            return False
