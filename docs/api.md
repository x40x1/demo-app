# Demo Mode Application API Documentation

This document provides a high level overview of the main classes exposed by the project.  The full reference can be found in the source code.

## Main Application Class
```python
class DemoModeApp:
    def __init__(self)
    def start_demo_mode(self)
    def stop_demo_mode(self)
    def add_content(self, type, path, duration=None)
    def remove_content(self, index)
    def get_status(self)
```

## Core Functionality
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

## Settings Management
```python
class SettingsManager:
    def get(self, key, default=None)
    def set(self, key, value)
    def hash_password(self, password)
    def verify_password(self, password, hash)
```

## Input Control
```python
class InputController:
    def start_monitoring(self)
    def stop_monitoring(self)
    def lock_keyboard(self)
    def unlock_keyboard(self)
```
