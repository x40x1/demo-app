"""
Demo Mode Application - Cross-Platform Demo Version
This version demonstrates the core functionality without Windows-specific features.
"""

import os
import sys
import json
import time
import threading
from datetime import datetime

# Mock Windows-specific modules for demonstration
class MockWinReg:
    HKEY_CURRENT_USER = "HKEY_CURRENT_USER"
    KEY_SET_VALUE = 1
    KEY_READ = 2
    REG_SZ = 1
    REG_DWORD = 4
    
    @staticmethod
    def OpenKey(key, subkey, reserved, access):
        return "mock_key"
    
    @staticmethod
    def SetValueEx(key, value_name, reserved, type, value):
        pass
    
    @staticmethod
    def QueryValueEx(key, value_name):
        return "mock_value", "type"
    
    @staticmethod
    def CloseKey(key):
        pass
    
    @staticmethod
    def DeleteValue(key, value_name):
        pass

# Mock ctypes for demonstration
class MockCtypes:
    windll = None

class DemoModeCore:
    """Core demo mode functionality without GUI dependencies"""
    
    def __init__(self):
        self.settings = self.load_settings()
        self.demo_content = []
        self.is_demo_active = False
        self.current_content_index = 0
        
    def load_settings(self):
        """Load settings from JSON file"""
        try:
            if os.path.exists("demo_settings.json"):
                with open("demo_settings.json", 'r') as f:
                    return json.load(f)
        except:
            pass
        
        return {
            'master_password_hash': None,
            'auto_start_demo': False,
            'photo_duration': 5,
            'video_duration': 30,
            'app_duration': 30,
            'inactivity_timeout': 30,
            'keyboard_lock_enabled': False,
            'demo_content': []
        }
    
    def save_settings(self):
        """Save settings to JSON file"""
        try:
            with open("demo_settings.json", 'w') as f:
                json.dump(self.settings, f, indent=2)
            return True
        except:
            return False
    
    def add_content(self, content_type, path, name=None, duration=None):
        """Add content to demo"""
        content_item = {
            'type': content_type,
            'path': path,
            'name': name or os.path.basename(path),
            'duration': duration or self.settings.get(f'{content_type}_duration', 10),
            'added_date': datetime.now().isoformat()
        }
        
        self.demo_content.append(content_item)
        self.settings['demo_content'] = self.demo_content
        self.save_settings()
        
        print(f"✅ Added {content_type}: {content_item['name']}")
    
    def remove_content(self, index):
        """Remove content by index"""
        if 0 <= index < len(self.demo_content):
            removed = self.demo_content.pop(index)
            self.settings['demo_content'] = self.demo_content
            self.save_settings()
            print(f"❌ Removed: {removed['name']}")
            return True
        return False
    
    def start_demo(self):
        """Start demo mode"""
        if not self.demo_content:
            print("⚠️  No demo content available. Add some content first.")
            return False
        
        self.is_demo_active = True
        self.current_content_index = 0
        
        print("🚀 Demo mode started!")
        print(f"📊 Content items: {len(self.demo_content)}")
        
        # Start demo loop
        self.demo_thread = threading.Thread(target=self._demo_loop, daemon=True)
        self.demo_thread.start()
        
        return True
    
    def stop_demo(self):
        """Stop demo mode"""
        self.is_demo_active = False
        print("🛑 Demo mode stopped!")
    
    def _demo_loop(self):
        """Main demo loop"""
        while self.is_demo_active and self.demo_content:
            content = self.demo_content[self.current_content_index]
            
            print(f"🎬 Playing: {content['name']} ({content['type']})")
            print(f"⏱️  Duration: {content['duration']} seconds")
            
            # Simulate content playback
            self._simulate_content_playback(content)
            
            # Move to next content
            self.current_content_index = (self.current_content_index + 1) % len(self.demo_content)
            
            # Wait for content duration
            time.sleep(content['duration'])
    
    def _simulate_content_playback(self, content):
        """Simulate content playback"""
        if content['type'] == 'photo':
            print(f"📸 Displaying photo: {content['path']}")
        elif content['type'] == 'video':
            print(f"🎥 Playing video: {content['path']}")
        elif content['type'] == 'application':
            print(f"🖥️  Launching application: {content['path']}")
        elif content['type'] == 'web':
            print(f"🌐 Opening web content: {content['path']}")
    
    def get_status(self):
        """Get current demo status"""
        return {
            'demo_active': self.is_demo_active,
            'content_count': len(self.demo_content),
            'current_content': self.current_content_index if self.demo_content else None,
            'settings_loaded': bool(self.settings)
        }
    
    def list_content(self):
        """List all demo content"""
        if not self.demo_content:
            print("📝 No demo content configured.")
            return
        
        print("\n📋 Demo Content:")
        print("-" * 50)
        for i, content in enumerate(self.demo_content):
            print(f"{i+1}. {content['name']}")
            print(f"   Type: {content['type']}")
            print(f"   Path: {content['path']}")
            print(f"   Duration: {content['duration']}s")
            print()

    def export_content(self, export_path):
        """Export demo content list to a JSON file"""
        try:
            with open(export_path, 'w') as f:
                json.dump(self.demo_content, f, indent=2)
            print(f"💾 Content exported to {export_path}")
            return True
        except Exception as e:
            print(f"❌ Failed to export content: {e}")
            return False

    def import_content(self, import_path):
        """Import demo content list from a JSON file"""
        try:
            with open(import_path, 'r') as f:
                self.demo_content = json.load(f)
            self.settings['demo_content'] = self.demo_content
            self.save_settings()
            print(f"📥 Imported content from {import_path}")
            return True
        except Exception as e:
            print(f"❌ Failed to import content: {e}")
            return False


def demo_interactive_session():
    """Interactive demo session"""
    print("🎭 Demo Mode Application - Interactive Demo")
    print("=" * 50)
    
    demo = DemoModeCore()
    
    # Add some sample content
    print("\n📥 Adding sample demo content...")
    demo.add_content('photo', '/path/to/product_showcase.jpg', 'Product Showcase', 8)
    demo.add_content('video', '/path/to/gaming_demo.mp4', 'Gaming Demo', 25)
    demo.add_content('application', '/path/to/demo_app.exe', 'Demo Application', 30)
    demo.add_content('web', 'https://example.com/product-demo', 'Web Demo', 20)
    
    print("\n📊 Current Status:")
    status = demo.get_status()
    for key, value in status.items():
        print(f"  {key}: {value}")
    
    print("\n📋 Demo Content List:")
    demo.list_content()
    
    print("\n🎬 Starting demo simulation...")
    demo.start_demo()

    # Let demo run for a few cycles
    print("⏳ Running demo for 15 seconds...")
    time.sleep(15)
    
    demo.stop_demo()

    # Export demo content to file
    export_path = "demo_export.json"
    demo.export_content(export_path)

    # Import it back (just for demonstration)
    demo.import_content(export_path)

    print("\n✅ Demo simulation completed!")
    print("\n📝 Next Steps for Production:")
    print("1. Install on Windows PC with Python")
    print("2. Add real content files (images, videos, apps)")
    print("3. Configure master password and security settings")
    print("4. Test full GUI application with 'python demo_app.py'")
    print("5. Create standalone executable for deployment")


if __name__ == "__main__":
    demo_interactive_session()