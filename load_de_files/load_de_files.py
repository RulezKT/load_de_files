import json
import os

FILES_DIR = "files"
DE_FILE = "de440s.bsp"
NODES_FILE = "nodes.json"
CERES_FILE = "ceres_typ21.bsp"
CHIRON_FILE = "chiron_typ21.bsp"


class FolderNotFound(Exception):
    pass


def _find_dir(files_dir: str) -> str:
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
def load_files() -> tuple[bytes, tuple[tuple[int, str]], bytes, bytes]:
    # print("load_files : starting loadinf files")
    dir_to_find = _find_dir(FILES_DIR)
    # print("load_files : directory found")
    de_path = os.path.join(dir_to_find, DE_FILE)
    file_in_mem = _load_de(de_path)
    # print("load_files : de file loaded")
    nodes_path = os.path.join(dir_to_find, NODES_FILE)
    nodes_file_data = _load_nodes(nodes_path)
    # print("load_files : nodes file loaded")

    ceres_path = os.path.join(dir_to_find, CERES_FILE)
    ceres_file = _load_de(ceres_path)

    chiron_path = os.path.join(dir_to_find, CHIRON_FILE)
    chiron_file = _load_de(chiron_path)

    return file_in_mem, nodes_file_data, ceres_file, chiron_file
