import argparse
from demo_core import DemoModeCore


def main():
    parser = argparse.ArgumentParser(description="Demo Mode command line interface")
    sub = parser.add_subparsers(dest="cmd")

    sub.add_parser("list", help="List configured demo content")

    add = sub.add_parser("add", help="Add demo content")
    add.add_argument("type", choices=["photo", "video", "application", "web"], help="Content type")
    add.add_argument("path", help="Path or URL to content")
    add.add_argument("name", nargs="?", help="Display name")
    add.add_argument("--duration", type=int, default=None, help="Duration in seconds")

    remove = sub.add_parser("remove", help="Remove content by index")
    remove.add_argument("index", type=int, help="Index of item to remove (1-based)")

    exp = sub.add_parser("export", help="Export content list to JSON")
    exp.add_argument("file", help="Output file")

    imp = sub.add_parser("import", help="Import content list from JSON")
    imp.add_argument("file", help="Input file")

    args = parser.parse_args()

    demo = DemoModeCore()

    if args.cmd == "list":
        demo.list_content()
    elif args.cmd == "add":
        demo.add_content(args.type, args.path, args.name, args.duration)
    elif args.cmd == "remove":
        demo.remove_content(args.index - 1)
    elif args.cmd == "export":
        demo.export_content(args.file)
    elif args.cmd == "import":
        demo.import_content(args.file)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
