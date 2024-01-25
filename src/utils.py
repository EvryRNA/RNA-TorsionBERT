import json
from typing import Dict


def read_fasta(in_path: str) -> str:
    """
    Read a fasta file to get the sequence
    :param in_path: path to a .fasta file
    :return: the RNA sequence
    """
    with open(in_path, "r") as f:
        lines = f.readlines()
    sequence = "".join([line.strip() for line in lines[1:]])
    return sequence


def save_json(content: Dict, path: str):
    """Save the dictionary into a json file.
    Args
    :param content: the object to save
    :param path: the path where to save. Could have .json or not in the path
    """
    assert type(content) is dict
    if path.endswith(".json"):
        path_to_save = path
    else:
        path_to_save = path + ".json"
    with open(path_to_save, "w") as file:
        json.dump(content, file)
