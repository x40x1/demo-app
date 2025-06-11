"""
Settings Manager - Handles configuration storage and encryption
"""

import json
import os
import hashlib
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class SettingsManager:
    def __init__(self, config_file="demo_config.json"):
        self.config_file = config_file
        self.settings = {}
        self.load_settings()
    
    def load_settings(self):
        """Load settings from file"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    self.settings = json.load(f)
            except (json.JSONDecodeError, IOError):
                self.settings = {}
        else:
            self.settings = {}
    
    def save_settings(self):
        """Save settings to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.settings, f, indent=2)
            return True
        except IOError:
            return False
    
    def get(self, key, default=None):
        """Get a setting value"""
        return self.settings.get(key, default)
    
    def set(self, key, value):
        """Set a setting value"""
        self.settings[key] = value
        self.save_settings()
    
    def hash_password(self, password):
        """Hash a password for secure storage"""
        salt = os.urandom(32)
        pwdhash = hashlib.pbkdf2_hmac('sha256', 
                                     password.encode('utf-8'), 
                                     salt, 
                                     100000)
        return base64.b64encode(salt + pwdhash).decode('ascii')
    
    def verify_password(self, password, stored_hash):
        """Verify a password against stored hash"""
        try:
            stored_bytes = base64.b64decode(stored_hash.encode('ascii'))
            salt = stored_bytes[:32]
            stored_hash_bytes = stored_bytes[32:]
            
            pwdhash = hashlib.pbkdf2_hmac('sha256',
                                         password.encode('utf-8'),
                                         salt,
                                         100000)
            return pwdhash == stored_hash_bytes
        except:
            return False
    
    def get_default_settings(self):
        """Get default settings"""
        return {
            'auto_start_demo': False,
            'photo_duration': 5,
            'keyboard_lock_enabled': False,
            'inactivity_timeout': 30,
            'windows_startup': False,
            'demo_content': [],
            'master_password': None
        }
    
    def reset_to_defaults(self):
        """Reset all settings to defaults"""
        self.settings = self.get_default_settings()
        self.save_settings()
