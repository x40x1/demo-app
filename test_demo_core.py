"""Additional tests for the Demo Mode core functionality."""

import os
from demo_core import DemoModeCore


def test_defaults():
    """Ensure default settings load correctly."""
    demo = DemoModeCore()
    defaults = demo.load_settings()
    assert 'auto_start_demo' in defaults
    assert defaults['photo_duration'] == 5
    assert isinstance(defaults['demo_content'], list)
    print("✅ DemoModeCore defaults loaded")


def test_add_content_and_status():
    """Test adding content updates status."""
    demo = DemoModeCore()
    demo.add_content('photo', '/tmp/test.jpg', 'test', 1)
    status = demo.get_status()
    assert status['content_count'] == 1
    assert demo.demo_content[0]['name'] == 'test'
    print("✅ DemoModeCore content addition")

def test_export_and_import():
    """Test exporting and importing content"""
    demo = DemoModeCore()
    demo.add_content('photo', '/tmp/test.jpg', 'export', 1)
    export_file = 'export_test.json'
    assert demo.export_content(export_file)

    demo.demo_content = []
    assert demo.import_content(export_file)
    assert len(demo.demo_content) == 1
    os.remove(export_file)
    print("✅ DemoModeCore export/import")


if __name__ == "__main__":
    all_passed = True
    for test in (test_defaults, test_add_content_and_status, test_export_and_import):
        try:
            test()
        except AssertionError as e:
            all_passed = False
            print(f"❌ {test.__name__} failed: {e}")
    if all_passed:
        print("🎉 demo_core tests passed")
    else:
        print("⚠️  Some demo_core tests failed")
