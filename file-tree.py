import os


def generate_tree(directory, prefix=""):
    """Recursively generate a file structure tree."""
    entries = sorted(os.listdir(directory))
    entries = [e for e in entries if not e.startswith(".")]  # Ignore hidden files

    for index, entry in enumerate(entries):
        path = os.path.join(directory, entry)
        is_last = index == len(entries) - 1
        connector = "└── " if is_last else "├── "

        print(prefix + connector + entry)

        if os.path.isdir(path):
            extension = "    " if is_last else "│   "
            generate_tree(path, prefix + extension)


if __name__ == "__main__":
    project_root = os.getcwd()  # Get current working directory (VS Code project root)
    print("Project Structure:\n")
    generate_tree(project_root)
