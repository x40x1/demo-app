"""
Simple test of the Demo Mode Application core functionality
This test runs the basic application components to verify they work correctly.
"""

import sys
import os
import time
import threading

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_settings_manager():
    """Test settings manager functionality"""
    print("Testing Settings Manager...")
    
    try:
        from settings_manager import SettingsManager
        
        # Create settings manager
        settings = SettingsManager("test_config.json")
        
        # Test basic get/set
        settings.set('test_key', 'test_value')
        value = settings.get('test_key')
        assert value == 'test_value', f"Expected 'test_value', got {value}"
        
        # Test password hashing
        password = "test123"
        hashed = settings.hash_password(password)
        assert settings.verify_password(password, hashed), "Password verification failed"
        assert not settings.verify_password("wrong", hashed), "Wrong password should fail"
        
        # Clean up
        if os.path.exists("test_config.json"):
            os.remove("test_config.json")
        
        print("✅ Settings Manager: PASSED")
        return True
        
    except Exception as e:
        print(f"❌ Settings Manager: FAILED - {e}")
        return False

def test_system_utils():
    """Test system utilities"""
    print("Testing System Utils...")
    
    try:
        from system_utils import SystemUtils
        
        # Create system utils
        sys_utils = SystemUtils()
        
        # Test system info (should work on any system)
        info = sys_utils.get_system_info()
        assert 'platform' in info, "System info missing platform"
        assert 'python_version' in info, "System info missing Python version"
        
        print("✅ System Utils: PASSED")
        return True
        
    except Exception as e:
        print(f"❌ System Utils: FAILED - {e}")
        return False

def test_application_components():
    """Test application components that don't require GUI"""
    print("Testing Application Components...")
    
    try:
        # Test imports
        from demo_app import DemoModeApp, ApplicationDialog, PasswordDialog
        from app_launcher import AppLauncher, KioskBrowser
        
        print("✅ Application Components: PASSED (imports successful)")
        return True
        
    except Exception as e:
        print(f"❌ Application Components: FAILED - {e}")
        return False

def test_input_controller_basic():
    """Test basic input controller functionality (without hooks)"""
    print("Testing Input Controller (basic)...")
    
    try:
        # Create mock app class
        class MockApp:
            def handle_escape_attempt(self):
                pass
            def on_activity_detected(self):
                pass
        
        from input_controller import InputController
        
        # Create input controller
        mock_app = MockApp()
        controller = InputController(mock_app)
        
        # Test basic functionality
        assert hasattr(controller, 'start_monitoring'), "Missing start_monitoring method"
        assert hasattr(controller, 'stop_monitoring'), "Missing stop_monitoring method"
        assert hasattr(controller, 'lock_keyboard'), "Missing lock_keyboard method"
        
        print("✅ Input Controller: PASSED (basic functionality)")
        return True
        
    except Exception as e:
        print(f"❌ Input Controller: FAILED - {e}")
        return False

def test_media_player_basic():
    """Test basic media player functionality"""
    print("Testing Media Player (basic)...")
    
    try:
        # Create mock app class
        class MockApp:
            def __init__(self):
                pass
        
        from media_player import MediaPlayer
        
        # Create media player
        mock_app = MockApp()
        player = MediaPlayer(mock_app)
        
        # Test basic functionality
        assert hasattr(player, 'play_content'), "Missing play_content method"
        assert hasattr(player, 'stop_playback'), "Missing stop_playback method"
        
        print("✅ Media Player: PASSED (basic functionality)")
        return True
        
    except Exception as e:
        print(f"❌ Media Player: FAILED - {e}")
        return False

def main():
    """Run all tests"""
    print("Demo Mode Application - Component Tests")
    print("=" * 50)
    
    tests = [
        test_settings_manager,
        test_system_utils,
        test_application_components,
        test_input_controller_basic,
        test_media_player_basic
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
    
    print("\n" + "=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The application components are working correctly.")
        print("\nNext Steps:")
        print("1. Run 'python demo_app.py' to start the full application")
        print("2. Test on a Windows machine for full keyboard lock functionality")
        print("3. Add your demo content (images, videos, applications)")
        print("4. Configure settings and test demo mode")
    else:
        print("⚠️  Some tests failed. Check the error messages above.")
        print("The application may still work, but some features might be limited.")
    
    return passed == total

if __name__ == "__main__":
    main()