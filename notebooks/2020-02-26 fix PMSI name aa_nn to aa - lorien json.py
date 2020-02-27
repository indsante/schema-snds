import os
import json

def get_files(folder: str, ext: str) -> list:
    """Get absolute path of all files endind with a given extension
    found in folder.

    :param folder: folder to parse for files.
    :param ext: extension of files to retrieve.
    :return: list of absolute paths to file.
    """

    files = []

    for dirpath, dirname, filenames in os.walk(folder):
        full_paths = [
            os.path.join(dirpath, filename) for filename in filenames
            if filename.endswith(ext)
        ]
        files.extend(full_paths)

    return files

def clean_up_files(files_list: list) -> dict:
    """Open all the files found at paths listed in files.

    Convert them as string.

    Returns dict of file content keyed by file path.

    :param files_list: list of absolute paths to file.
    :return: dict containing the file's path as key and a list containing
        each line as value.
    """

    files = {}

    for file_path in files_list:
        with open(file_path) as file:
            raw = json.load(file)
            data = json.dumps(raw)
            files[file_path] = data

    return files

def replace_text(replace: str, substitute: str, files: dict) -> dict:
    """Replace substring in every file.

    Returns dict of modified file content keyed by file path.

    :param replace: old substring to replace.
    :param substitute: new substring which would replace the old substring.
    :param files: files to check.
    :return: dict containing the file's path as key and a modified file content
    with replaced substring as value.
    """

    fixed_files = {file_path: file.replace(replace, substitute)
                    for file_path, file in files.items()
                    }

    return fixed_files

def write_files(files: dict, replace: str, substitute: str):
    """Rename modified files by replacing substring and save them under
    new path.

    Delete old files.

    :param files: modified files with replaced substring.
    """

    for file_path, file_contents in files.items():
        json_contents = json.loads(file_contents)
        rename = file_path.replace(replace, substitute)
        with open(rename, 'w') as file:
            json.dump(json_contents, file, indent=4, ensure_ascii=False)
        if os.path.exists(file_path) and file_path != rename:
            os.remove(file_path)


def main (
        folder : str = '../schemas',
        ext = '.json',
        replace: str = 'aa_nn',
        substitute: str = 'aa'
):

    file_paths = get_files(folder, ext)
    clean_files = clean_up_files(file_paths)
    fixed_files = replace_text(replace, substitute, clean_files)
    write_files(fixed_files, replace, substitute)

if __name__ == '__main__':
    main()
