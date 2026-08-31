from pathlib import Path


def inspect_files(source_folder):
    """Return the names of files in the source folder."""

    files = []

    for file in source_folder.iterdir():

        if file.is_file():
            files.append(file.name)

    return files


if __name__ == "__main__":

    source_folder = Path("source")

    for file_name in inspect_files(source_folder):
        print(file_name)