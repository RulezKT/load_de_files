import json
import os

FILES_DIR = "files"
DE_FILE = "de440s.bsp"
NODES_FILE = "nodes.json"


class FolderNotFound(Exception):
    pass


def __find_dir(files_dir: str) -> str:
    # The __file__ var contains the absolute path of the executing script
    current_directory = os.path.dirname(__file__)

    while True:
        dir_to_find = os.path.join(current_directory, files_dir)
        if os.path.exists(dir_to_find):
            return dir_to_find

        if current_directory == "/" or current_directory == os.path.dirname(
            current_directory
        ):
            raise FolderNotFound("There is no '/files' directory" + current_directory)

        current_directory = os.path.dirname(current_directory)


def _load_de(path: str) -> bytes:
    file_in_mem = None
    try:
        with open(path, "rb") as fp:
            file_in_mem = fp.read()

    except (FileNotFoundError, PermissionError) as e:
        print(f"Error: {e}")

    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")

    return file_in_mem


def _load_nodes(path: str) -> tuple[tuple[int, str]]:
    file_in_mem = None
    try:
        with open(path, "r") as fs:
            file_in_mem = json.loads(fs.read())
    except (FileNotFoundError, PermissionError) as e:
        print(f"Error: {e}")

    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")

    return file_in_mem


# bytes for de440s.bsp,
# tuple[tuple[int, str] for nodes.json  # [-4733494022,"north"],[-4732252235,"south"]
def load_files() -> tuple[bytes, tuple[tuple[int, str]]]:
    dir_to_find = __find_dir(FILES_DIR)
    de_path = os.path.join(dir_to_find, DE_FILE)
    file_in_mem = _load_de(de_path)
    nodes_path = os.path.join(dir_to_find, NODES_FILE)
    nodes_file_data = _load_nodes(nodes_path)

    return file_in_mem, nodes_file_data
