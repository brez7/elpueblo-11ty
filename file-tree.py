import os


def generate_tree(directory, prefix="", skip_dirs=None, output_lines=None):
    """Recursively generate a file structure tree."""
    if skip_dirs is None:
        skip_dirs = {"node_modules", "__pycache__"}
    if output_lines is None:
        output_lines = []

    entries = sorted(os.listdir(directory))
    entries = [e for e in entries if not e.startswith(".")]

    for index, entry in enumerate(entries):
        path = os.path.join(directory, entry)
        if entry in skip_dirs:
            continue

        is_last = index == len(entries) - 1
        connector = "└── " if is_last else "├── "
        output_lines.append(prefix + connector + entry)

        if os.path.isdir(path):
            extension = "    " if is_last else "│   "
            generate_tree(path, prefix + extension, skip_dirs, output_lines)

    return output_lines


if __name__ == "__main__":
    project_root = os.getcwd()
    tree_output = generate_tree(project_root)

    output_file = "file_tree.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("Project Structure:\n\n")
        f.write("\n".join(tree_output))

    print(f"File tree saved to: {output_file}")
