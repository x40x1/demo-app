# Demo Mode Application for Retail Environments

![Demo Mode](https://img.shields.io/badge/Platform-Windows-blue) ![Python](https://img.shields.io/badge/Python-3.8+-green) ![License](https://img.shields.io/badge/License-MIT-yellow)

A comprehensive retail demo application designed for environments like MediaMarkt to showcase PCs. The application provides full-screen demonstrations with advanced security features, content management, and kiosk-mode functionality.

## 🚀 Key Features

### Core Functionality
- **Full-Screen Demo Mode**: Immersive content display that takes over the entire screen
- **Multi-Content Support**: Photos, videos, desktop applications, and web content
- **Automatic Content Rotation**: Seamless looping through demo content
- **Inactivity Detection**: Returns to full-screen mode after user inactivity

### Security Features
- **Master Password Protection**: Secure access to settings and configuration
- **Keyboard Lock**: Complete keyboard disable with admin privileges
- **Emergency Escape**: Ctrl+Alt+Shift+Esc combination for staff access
- **Kiosk Mode**: Prevents unauthorized access to system functions

### Content Management
- **Drag & Drop Interface**: Easy content addition and management
- **Multiple Media Formats**: Support for common image and video formats
- **Application Launcher**: Launch desktop applications and web demos
- **Configurable Timing**: Individual duration settings for each content type

### System Integration
- **Auto-Startup**: Automatic launch with Windows boot
- **Power Management**: Prevents screen saver and system sleep
- **Registry Integration**: Professional Windows integration
- **Standalone Executable**: No Python installation required for deployment

## 📋 System Requirements

### Minimum Requirements
- Windows 10 or later
- 4GB RAM
- 1GB storage space
- Display resolution: 1920x1080 (recommended)

### For Development
- Python 3.8 or later
- Administrator privileges (for full functionality)
- Internet connection (for web content)

### Recommended Hardware
- Intel Core i5 or equivalent
- 8GB RAM
- SSD storage
- Dedicated graphics card (for video content)
- Touch screen (for interactive demos)

## 🛠️ Installation

### Option 1: Automated Windows Installation
```batch
# Download and run the installer
install_windows.bat
```

### Option 2: Manual Installation
```bash
# Install Python dependencies
pip install -r requirements.txt

# Install Windows-specific packages
pip install pywin32 win32com.client

# Run the application
python demo_app.py
```

### Option 3: Standalone Executable
```bash
# Create executable
pyinstaller --onefile --windowed --name DemoModeApp demo_app.py

# Deploy to target PCs
copy dist/DemoModeApp.exe [target_location]
```

## 🎯 Quick Start Guide

### 1. Initial Setup
1. Launch the application
2. Click "Settings" and set up master password
3. Configure basic preferences (timing, security level)

### 2. Add Demo Content
```
Content Types Supported:
├── Images: JPG, PNG, GIF, BMP
├── Videos: MP4, AVI, MOV, WMV, MKV
├── Applications: Any Windows executable
└── Web Content: URLs for browser-based demos
```

### 3. Start Demo Mode
1. Click "Start Demo Mode"
2. Application enters full-screen mode
3. Content begins automatic rotation
4. Use emergency escape (Ctrl+Alt+Shift+Esc) to exit

## 🔧 Configuration Options

### Security Settings
```python
Security Levels:
├── Basic: Prevents common exit keys
├── Enhanced: Keyboard lock with admin privileges  
├── Kiosk: Complete system lockdown
└── Emergency: Always-available escape combination
```

### Content Settings
```python
Content Configuration:
├── Display Duration: Per-content timing
├── Transition Effects: Smooth content switching
├── Loop Behavior: Continuous or scheduled rotation
└── Content Scheduling: Time-based content display
```

### System Settings
```python
System Integration:
├── Auto-Startup: Launch with Windows
├── Power Management: Prevent sleep/screensaver
├── Registry Integration: Professional installation
└── Monitoring: Application and system monitoring
```

## 📁 Project Structure

```
DemoModeApp/
├── demo_app.py              # Main application entry point
├── settings_manager.py      # Configuration and security management
├── input_controller.py      # Keyboard/mouse input handling
├── media_player.py          # Photo and video playback
├── app_launcher.py          # Application and web content launcher
├── system_utils.py          # Windows system integration
├── demo_core.py            # Cross-platform demo core
├── test_demo_app.py        # Component testing
├── requirements.txt        # Python dependencies
├── install_windows.bat     # Automated installer
├── DEPLOYMENT_GUIDE.md     # Comprehensive deployment guide
└── README.md              # This file
```

## 🔒 Security Features

### Access Control
- **Master Password**: Required for all configuration changes
- **Role-Based Access**: Staff vs. customer interaction levels
- **Session Management**: Automatic security timeouts

### System Protection
- **Keyboard Lock**: Disable system keys and shortcuts
- **Process Management**: Monitor and control running applications
- **Registry Protection**: Secure system integration

### Emergency Procedures
- **Emergency Escape**: Ctrl+Alt+Shift+Esc + master password
- **Remote Management**: Network-based control (optional)
- **Logging**: Complete activity and security logging

## 🎨 Content Management

### Supported Content Types

#### Images
- **Formats**: JPG, JPEG, PNG, GIF, BMP
- **Features**: Auto-resize, aspect ratio preservation
- **Configuration**: Individual display duration

#### Videos
- **Formats**: MP4, AVI, MOV, WMV, MKV
- **Features**: Full-screen playback, audio support
- **Configuration**: Loop control, volume settings

#### Applications
- **Type**: Windows executables (.exe)
- **Features**: Automatic launching and closing
- **Configuration**: Duration limits, process monitoring

#### Web Content
- **Type**: URLs and web applications
- **Features**: Kiosk browser mode, tab management
- **Configuration**: Timeout settings, security restrictions

### Content Organization
```
Recommended Directory Structure:
content/
├── images/
│   ├── product_showcase/
│   ├── promotional/
│   └── branding/
├── videos/
│   ├── product_demos/
│   ├── tutorials/
│   └── commercials/
└── applications/
    ├── games/
    ├── software_demos/
    └── interactive/
```

## 🔧 Advanced Configuration

### Kiosk Mode Setup
```python
# Complete kiosk configuration
kiosk_settings = {
    'keyboard_lock': True,
    'hide_taskbar': True,
    'disable_alt_tab': True,
    'prevent_task_manager': True,
    'auto_restart_on_crash': True
}
```

### Performance Optimization
```python
# Performance settings
performance_config = {
    'hardware_acceleration': True,
    'memory_management': 'aggressive',
    'content_preloading': True,
    'cpu_priority': 'high'
}
```

### Network Configuration
```python
# Network and web content settings
network_settings = {
    'web_content_timeout': 30,
    'browser_cache_size': '500MB',
    'content_filtering': True,
    'offline_fallback': True
}
```

## 📊 Monitoring and Analytics

### Application Monitoring
- **Performance Metrics**: CPU, memory, storage usage
- **Content Analytics**: View time, interaction rates
- **Error Logging**: Comprehensive error tracking
- **System Health**: Hardware and software status

### Reporting Features
- **Usage Reports**: Daily, weekly, monthly summaries
- **Content Performance**: Most/least viewed content
- **System Status**: Uptime, crashes, maintenance needs
- **Security Events**: Access attempts, configuration changes

## 🚀 Deployment Scenarios

### Single PC Setup
```
Ideal for: Individual demo stations
Setup time: 15 minutes
Features: Full functionality, local content
Maintenance: Monthly content updates
```

### Multi-PC Network
```
Ideal for: Store-wide deployments
Setup time: 1-2 hours
Features: Centralized management, synchronized content
Maintenance: Remote updates, monitoring dashboard
```

### Kiosk Installation
```
Ideal for: Unattended demonstrations
Setup time: 30 minutes
Features: Maximum security, automatic recovery
Maintenance: Minimal, self-healing configuration
```

## 🛠️ Troubleshooting

### Common Issues and Solutions

#### Application Won't Start
```bash
# Check Python installation
python --version

# Verify dependencies
pip list | findstr "pygame\|pillow\|opencv"

# Run in debug mode
python demo_app.py --debug
```

#### Keyboard Lock Not Working
```
Solution: Run as Administrator
1. Right-click application
2. Select "Run as administrator"
3. Accept UAC prompt
```

#### Video Playback Issues
```
Solution: Install media codecs
1. Download K-Lite Codec Pack
2. Install with default settings
3. Restart application
```

#### Performance Problems
```
Solution: Optimize settings
1. Reduce video quality/resolution
2. Decrease content duration
3. Close unnecessary background apps
4. Check hardware requirements
```

### Logging and Diagnostics
```python
# Enable detailed logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Check system status
python -c "from system_utils import SystemUtils; print(SystemUtils().get_system_info())"

# Test components individually
python test_demo_app.py
```

## 📚 API Reference

### Main Application Class
```python
class DemoModeApp:
    def __init__(self)
    def start_demo_mode(self)
    def stop_demo_mode(self)
    def add_content(self, type, path, duration=None)
    def remove_content(self, index)
    def get_status(self)
```

### Settings Management
```python
class SettingsManager:
    def get(self, key, default=None)
    def set(self, key, value)
    def hash_password(self, password)
    def verify_password(self, password, hash)
```

### Input Control
```python
class InputController:
    def start_monitoring(self)
    def stop_monitoring(self)
    def lock_keyboard(self)
    def unlock_keyboard(self)
```

### Core Module
```python
class DemoModeCore:
    def add_content(self, content_type, path, name=None, duration=None)
    def remove_content(self, index)
    def list_content(self)
    def export_content(self, export_path)
    def import_content(self, import_path)
    def start_demo(self)
    def stop_demo(self)
    def get_status(self)
```

## ⌨️ Command Line Interface

Use `cli.py` to manage demo content without launching the GUI:

```bash
# List configured content
python cli.py list

# Add a photo
python cli.py add photo /path/to/image.jpg "Storefront" --duration 10

# Export all items
python cli.py export demo_content.json
```

## 🤝 Contributing

### Development Setup
```bash
# Clone repository
git clone https://github.com/x40x1/demo_app.git #adding later

# Install development dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Run tests
python test_demo_app.py

# Run linting
flake8 *.py
```

### Code Style
- Follow PEP 8 guidelines
- Use type hints where appropriate
- Comprehensive docstrings for all functions
- Unit tests for new features

### Submitting Changes
1. Fork the repository
2. Create feature branch
3. Make changes with tests
4. Submit pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

### Documentation
- [Deployment Guide](DEPLOYMENT_GUIDE.md)
- [API Documentation](docs/api.md)
- [Troubleshooting Guide](docs/troubleshooting.md)

### Community
- [GitHub Issues](https://github.com/x40x1/demo-app/issues)

---

**Demo Mode Application** - Professional retail demonstration software for showcasing PCs and technology products in store environments.

Built with ❤️ for retail technology demonstrations.
