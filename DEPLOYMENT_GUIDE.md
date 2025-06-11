# Demo Mode Application - Deployment Guide

## Overview
This Demo Mode Application is designed for retail environments like MediaMarkt to showcase PCs. It provides full-screen demos with keyboard lock functionality and automatic content rotation.

## Features
- ✅ Full-screen mode with keyboard lock
- ✅ Application launcher for desktop apps and web content
- ✅ Photo and video playback in loops
- ✅ Automatic hiding on mouse/keyboard activity
- ✅ Master password protection for settings
- ✅ Emergency escape combination (Ctrl+Alt+Shift+Esc)
- ✅ Auto-startup with Windows
- ✅ Inactivity detection for returning to demo mode

## System Requirements

### Minimum Requirements
- Windows 10 or later
- Python 3.8+ (for development)
- 4GB RAM
- 1GB storage space
- Internet connection (for web content)

### For Production Deployment
- Windows 10/11 Pro (recommended for kiosk features)
- Administrator privileges (for keyboard lock and startup configuration)
- Dedicated demo PC per application instance

## Installation Methods

### Method 1: Development Installation (Testing)

1. **Install Python 3.8+**
   ```bash
   # Download from python.org
   # Ensure Python is added to PATH
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   
   # For Windows-specific features, also install:
   pip install pywin32
   pip install win32com
   ```

3. **Run Application**
   ```bash
   python demo_app.py
   ```

### Method 2: Standalone Executable (Production)

1. **Create Executable**
   ```bash
   # Install PyInstaller
   pip install pyinstaller
   
   # Create standalone executable
   pyinstaller --onefile --windowed --name DemoModeApp demo_app.py
   
   # Executable will be in dist/ folder
   ```

2. **Deploy to Target PC**
   - Copy `DemoModeApp.exe` to target PC
   - Copy any demo content (videos, images) to the PC
   - Run executable as Administrator for full functionality

### Method 3: Windows Installer Package

1. **Create Installer (Advanced)**
   ```bash
   # Use tools like NSIS or Inno Setup to create installer
   # Include all dependencies and content files
   ```

## Configuration

### Initial Setup

1. **First Run**
   - Launch application
   - Click "Settings" to configure
   - Set master password (required for security)
   - Configure demo content paths
   - Set timing preferences

2. **Add Demo Content**
   - **Photos**: JPG, PNG, GIF, BMP formats
   - **Videos**: MP4, AVI, MOV, WMV, MKV formats
   - **Applications**: Desktop executables or web URLs
   - **Duration**: Configure display time for each content type

3. **Security Settings**
   - Set master password (minimum 4 characters)
   - Enable keyboard lock (requires admin privileges)
   - Configure emergency escape combination

### Advanced Configuration

#### Keyboard Lock Levels
1. **Basic Lock**: Prevents common keys (Ctrl+Alt+Del disabled)
2. **Complete Lock**: Requires administrator privileges
3. **Emergency Escape**: Ctrl+Alt+Shift+Esc always works

#### Auto-Startup Configuration
1. Enable "Start with Windows" in settings
2. Application will start automatically on boot
3. Can immediately enter demo mode if configured

#### Power Management
- Automatically disables screen saver
- Prevents system sleep during demo
- Configurable inactivity timeouts

## Usage Instructions

### For Store Staff

1. **Starting Demo Mode**
   - Launch application
   - Add demo content (photos, videos, applications)
   - Click "Start Demo Mode"
   - Application goes fullscreen and begins content rotation

2. **Accessing Settings During Demo**
   - Press Ctrl+Alt+Shift+Esc
   - Enter master password
   - Access settings or stop demo

3. **Emergency Stop**
   - Same as accessing settings
   - Use "Stop Demo Mode" button

### For Customers

- Content plays automatically in fullscreen
- Touch screen or move mouse to see available options
- Application returns to fullscreen after inactivity
- Cannot access system functions when keyboard is locked

## Content Management

### Supported Content Types

1. **Images**
   - Formats: JPG, JPEG, PNG, GIF, BMP
   - Auto-resize to fit screen
   - Configurable display duration

2. **Videos**
   - Formats: MP4, AVI, MOV, WMV, MKV
   - Auto-loop playback
   - Full-screen scaling

3. **Desktop Applications**
   - Launch any Windows executable
   - Automatic closing after set duration
   - Monitor for crashes and restart

4. **Web Content**
   - Open URLs in browser
   - Support for kiosk mode browsers
   - Automatic tab management

### Content Organization

```
Demo Content Structure:
├── images/
│   ├── product_showcase.jpg
│   ├── store_promotion.png
│   └── brand_logos.gif
├── videos/
│   ├── product_demo.mp4
│   ├── gaming_showcase.avi
│   └── feature_highlights.mov
└── applications/
    ├── game_demo.exe
    ├── software_trial.exe
    └── web_demos.txt (URLs)
```

## Security Considerations

### Access Control
- Master password protects all settings
- Emergency escape requires password
- Settings accessible only to authorized staff

### System Security
- Application runs in user space (unless keyboard lock enabled)
- No permanent system changes (except startup registry)
- All changes reversible through settings

### Network Security
- Web content filtered through default browser security
- No external network access required for local content
- Optional: Configure firewall rules for web content

## Troubleshooting

### Common Issues

1. **Keyboard Lock Not Working**
   - Run as Administrator
   - Check Windows User Account Control settings
   - Verify admin privileges

2. **Video Playback Issues**
   - Install media codecs (K-Lite Codec Pack recommended)
   - Check video file formats
   - Verify hardware acceleration

3. **Application Crashes**
   - Check Python dependencies
   - Verify file paths in configuration
   - Review error logs

4. **Auto-Startup Not Working**
   - Check Windows startup programs
   - Verify registry permissions
   - Run initial setup as Administrator

### Performance Optimization

1. **Hardware Recommendations**
   - SSD for faster content loading
   - Dedicated graphics card for video content
   - Minimum 8GB RAM for smooth operation

2. **Software Optimization**
   - Close unnecessary background applications
   - Disable Windows updates during demo hours
   - Configure power settings for high performance

### Maintenance

1. **Regular Tasks**
   - Update demo content monthly
   - Check for application updates
   - Clean temporary files

2. **Monitoring**
   - Check system performance
   - Monitor for application crashes
   - Verify content file integrity

## Support and Updates

### Getting Help
1. Check this documentation first
2. Review error logs and console output
3. Test with minimal configuration
4. Contact system administrator

### Updates and Maintenance
- Regular content updates recommended
- Application updates as needed
- System maintenance during off-hours

## Legal and Compliance

### Content Licensing
- Ensure all demo content is properly licensed
- Respect copyright for videos and images
- Verify software demonstration permissions

### Data Protection
- No personal data collection by default
- Settings stored locally only
- Comply with local privacy regulations

### Accessibility
- Support for various screen sizes
- Configurable content duration
- Audio/visual accessibility options

---

## Quick Start Checklist

- [ ] Install Python and dependencies
- [ ] Run application for first time
- [ ] Set master password
- [ ] Add demo content (images, videos, apps)
- [ ] Test demo mode functionality
- [ ] Configure auto-startup if needed
- [ ] Test emergency escape procedure
- [ ] Create backup of configuration
- [ ] Deploy to production PCs
- [ ] Train store staff on usage

**Note**: This application is designed for controlled retail environments. Always test thoroughly before production deployment.