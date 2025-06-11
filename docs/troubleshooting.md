# Troubleshooting Guide

This guide lists common issues encountered when running the demo application and the recommended steps to resolve them.

## Application Won't Start
```bash
# Check Python installation
python --version

# Verify dependencies
pip list | findstr "pygame\|pillow\|opencv"

# Run in debug mode
python demo_app.py --debug
```

## Keyboard Lock Not Working
```
Solution: Run as Administrator
1. Right-click application
2. Select "Run as administrator"
3. Accept UAC prompt
```

## Video Playback Issues
```
Solution: Install media codecs
1. Download K-Lite Codec Pack
2. Install with default settings
3. Restart application
```

## Performance Problems
```
Solution: Optimize settings
1. Reduce video quality/resolution
2. Decrease content duration
3. Close unnecessary background apps
4. Check hardware requirements
```

## Logging and Diagnostics
```python
# Enable detailed logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Check system status
python -c "from system_utils import SystemUtils; print(SystemUtils().get_system_info())"

# Test components individually
python test_demo_app.py
```
