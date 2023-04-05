"""Prints out Python files and the number of nodes in them, in descending order."""
import argparse
import ast
import os.path
from pathlib import Path
from typing import Iterator, NamedTuple


def yellow(text: str) -> None:
    print(f"\033[33m{text}\033[m")


def find_all_python_files_in_folder(folder_path: str) -> Iterator[str]:
    for path in Path(folder_path).rglob("*.py"):
        if any(part in str(path) for part in ("venv", ".tox")):
            continue  # skipping these folders entirely for now
        if path.is_file():
            yield str(path)


class FileCount(NamedTuple):
    file_path: str
    node_count: int


def get_file_node_count(file_path: str) -> FileCount | None:
    with open(file_path) as file:
        try:
            tree = ast.parse(file.read())
        except (SyntaxError, ValueError):
            return None  # these files have invalid code

    node_count = 0
    for _ in ast.walk(tree):
        node_count += 1

    return FileCount(file_path, node_count)


class ArgNamespace:
    files_or_folders: str


parser = argparse.ArgumentParser()
parser.add_argument("files_or_folders", nargs="+")
args = parser.parse_args(namespace=ArgNamespace)


def main() -> None:
    file_node_counts: list[FileCount] = []
    for file_or_folder in args.files_or_folders:
        if os.path.isdir(file_or_folder):
            for file_path in find_all_python_files_in_folder(file_or_folder):
                file_node_count = get_file_node_count(file_path)
                if file_node_count is not None:
                    file_node_counts.append(file_node_count)

        elif os.path.isfile(file_or_folder):
            file_node_count = get_file_node_count(file_or_folder)
            if file_node_count is not None:
                file_node_counts.append(file_node_count)

        else:
            yellow(f"Skipping {file_or_folder} as the path does not exist.")

    file_node_counts.sort(key=lambda file: file.node_count, reverse=True)
    longest_named_file = max(file_node_counts, key=lambda file: len(file.file_path))
    longest_name = len(longest_named_file.file_path)
    for file in file_node_counts:
        print(f"{file.file_path:{longest_name}}{file.node_count:>10,} nodes")


if __name__ == "__main__":
    main()
