"""
Input Controller - Handles keyboard and mouse monitoring and control
"""

import threading
import time
import ctypes
import ctypes.wintypes
from ctypes import wintypes
import sys

# Windows API constants
WH_KEYBOARD_LL = 13
WH_MOUSE_LL = 14
WM_KEYDOWN = 0x0100
WM_KEYUP = 0x0101
WM_MOUSEMOVE = 0x0200
WM_LBUTTONDOWN = 0x0201
WM_RBUTTONDOWN = 0x0204

# Virtual key codes
VK_CONTROL = 0x11
VK_MENU = 0x12  # Alt key
VK_SHIFT = 0x10
VK_ESCAPE = 0x1B

class InputController:
    def __init__(self, app):
        self.app = app
        self.monitoring = False
        self.keyboard_locked = False
        self.mouse_locked = False
        
        # Hook handles
        self.keyboard_hook = None
        self.mouse_hook = None
        
        # Pressed keys tracking
        self.pressed_keys = set()
        
        # Windows API setup
        self.user32 = ctypes.windll.user32
        self.kernel32 = ctypes.windll.kernel32
        
        # Hook procedure types
        self.HOOKPROC = ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.c_int, wintypes.WPARAM, wintypes.LPARAM)
        
        # Hook procedures
        self.keyboard_proc = self.HOOKPROC(self._keyboard_hook_proc)
        self.mouse_proc = self.HOOKPROC(self._mouse_hook_proc)
    
    def start_monitoring(self):
        """Start monitoring keyboard and mouse input"""
        if self.monitoring:
            return
        
        self.monitoring = True
        
        # Start monitoring thread
        self.monitor_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        self.monitor_thread.start()
    
    def stop_monitoring(self):
        """Stop monitoring input"""
        self.monitoring = False
        
        # Unhook if hooks are installed
        if self.keyboard_hook:
            self.user32.UnhookWindowsHookExW(self.keyboard_hook)
            self.keyboard_hook = None
        
        if self.mouse_hook:
            self.user32.UnhookWindowsHookExW(self.mouse_hook)
            self.mouse_hook = None
    
    def lock_keyboard(self):
        """Lock keyboard input (requires admin privileges for complete lock)"""
        self.keyboard_locked = True
        
        # Install low-level keyboard hook
        if not self.keyboard_hook:
            self.keyboard_hook = self.user32.SetWindowsHookExW(
                WH_KEYBOARD_LL,
                self.keyboard_proc,
                self.kernel32.GetModuleHandleW(None),
                0
            )
    
    def unlock_keyboard(self):
        """Unlock keyboard input"""
        self.keyboard_locked = False
        
        # Remove keyboard hook
        if self.keyboard_hook:
            self.user32.UnhookWindowsHookExW(self.keyboard_hook)
            self.keyboard_hook = None
    
    def lock_mouse(self):
        """Lock mouse input"""
        self.mouse_locked = True
        
        # Install low-level mouse hook
        if not self.mouse_hook:
            self.mouse_hook = self.user32.SetWindowsHookExW(
                WH_MOUSE_LL,
                self.mouse_proc,
                self.kernel32.GetModuleHandleW(None),
                0
            )
    
    def unlock_mouse(self):
        """Unlock mouse input"""
        self.mouse_locked = False
        
        # Remove mouse hook
        if self.mouse_hook:
            self.user32.UnhookWindowsHookExW(self.mouse_hook)
            self.mouse_hook = None
    
    def _keyboard_hook_proc(self, nCode, wParam, lParam):
        """Low-level keyboard hook procedure"""
        if nCode >= 0:
            # Get virtual key code
            vk_code = ctypes.cast(lParam, ctypes.POINTER(ctypes.c_ulong)).contents.value & 0xFFFFFFFF
            
            # Track key presses for escape combination
            key_name = self._get_key_name(vk_code)
            
            if wParam == WM_KEYDOWN:
                if key_name:
                    self.pressed_keys.add(key_name.lower())
                    
                # Check for escape combination
                escape_keys = {'ctrl', 'alt', 'shift', 'esc'}
                if escape_keys.issubset(self.pressed_keys):
                    # Allow escape combination to pass through
                    self.app.handle_escape_attempt()
                    return self.user32.CallNextHookEx(None, nCode, wParam, lParam)
                
            elif wParam == WM_KEYUP:
                if key_name and key_name.lower() in self.pressed_keys:
                    self.pressed_keys.discard(key_name.lower())
            
            # Block all other keys if keyboard is locked
            if self.keyboard_locked:
                # Allow escape combination
                escape_keys = {'ctrl', 'alt', 'shift', 'esc'}
                if not escape_keys.issubset(self.pressed_keys):
                    return 1  # Block the key
        
        return self.user32.CallNextHookEx(None, nCode, wParam, lParam)
    
    def _mouse_hook_proc(self, nCode, wParam, lParam):
        """Low-level mouse hook procedure"""
        if nCode >= 0:
            # Detect mouse activity for demo mode
            if wParam in [WM_MOUSEMOVE, WM_LBUTTONDOWN, WM_RBUTTONDOWN]:
                if not self.mouse_locked:
                    self.app.on_activity_detected()
                
                # Block mouse if locked
                if self.mouse_locked:
                    return 1  # Block the mouse event
        
        return self.user32.CallNextHookEx(None, nCode, wParam, lParam)
    
    def _get_key_name(self, vk_code):
        """Get key name from virtual key code"""
        key_map = {
            VK_CONTROL: 'ctrl',
            VK_MENU: 'alt',
            VK_SHIFT: 'shift',
            VK_ESCAPE: 'esc'
        }
        return key_map.get(vk_code)
    
    def _monitoring_loop(self):
        """Main monitoring loop"""
        while self.monitoring:
            # Process Windows messages
            try:
                msg = wintypes.MSG()
                bRet = self.user32.GetMessageW(ctypes.byref(msg), None, 0, 0)
                
                if bRet == 0:  # WM_QUIT
                    break
                elif bRet == -1:  # Error
                    break
                else:
                    self.user32.TranslateMessage(ctypes.byref(msg))
                    self.user32.DispatchMessageW(ctypes.byref(msg))
                    
            except Exception as e:
                print(f"Error in monitoring loop: {e}")
                break
            
            time.sleep(0.01)  # Small delay to prevent high CPU usage


class KeyboardMonitor:
    """Simple keyboard activity monitor (fallback for non-admin scenarios)"""
    def __init__(self, app):
        self.app = app
        self.monitoring = False
        self.last_activity = time.time()
    
    def start_monitoring(self):
        """Start simple keyboard monitoring"""
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
    
    def stop_monitoring(self):
        """Stop monitoring"""
        self.monitoring = False
    
    def _monitor_loop(self):
        """Simple monitoring loop using GetAsyncKeyState"""
        user32 = ctypes.windll.user32
        
        while self.monitoring:
            # Check for any key press
            for vk in range(1, 256):
                if user32.GetAsyncKeyState(vk) & 0x8000:
                    current_time = time.time()
                    if current_time - self.last_activity > 0.1:  # Debounce
                        self.app.on_activity_detected()
                        self.last_activity = current_time
                    break
            
            time.sleep(0.1)
