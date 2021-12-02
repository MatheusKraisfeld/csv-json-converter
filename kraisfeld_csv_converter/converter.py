import logging
from pathlib import Path
from typing import Tuple

import click
import pandas as pd

logging.basicConfig(level="DEBUG", format="'%(asctime)s - %(name)s - %(levelname)s - %(message)s'")
logger = logging.getLogger(__name__)


@click.command()
@click.option(
    "--input",
    "-i",
    default="./",
    help="Path where to find CSV files to be converted to JSON.",
    type=str,
)
@click.option(
    "--output",
    "-o",
    default="./",
    help="Path where the converted files will be saved.",
    type=str,
)
@click.option(
    "--delimiter",
    "-d",
    default=",",
    help="Separator used to split the files.",
    type=str,
)
@click.option(
    "--prefix",
    "-p",
    prompt=True,
    prompt_required=False,
    default="file",
    help=(
        "Prefix used to prepend to the name of the converted file saved on disk."
        " The suffix will be a number starting from 0. ge: file_0.json."
    ),
    type=str,
)
def converter(input: str = "./", output: str = "./", delimiter: str = ",", prefix: str = None):
    input_path = Path(input)
    output_path = Path(output)
    logger.info("Input Path: %s", input_path)
    logger.info("Output Path: %s", output_path)

    for p in [input_path, output_path]:
        if not (p.is_file() or p.is_dir()):
            raise TypeError("Not a valid path of file name.")

    data = read_csv_file(source=input_path, delimiter=delimiter)
    # save_to_json_files(csvs=data, output_path=output_path, prefix=prefix)


def read_csv_file(source: Path, delimiter: str = ",") -> list:
    """Load a single csv file or all files withing a directory.

    Args:
        source (Path): Path for a single file or directory with files.
        delimiter (str, optional): Separator columns in the csv`s. Defaults to ','.

    Returns:
        list[list[str]]: All dataframes loaded from the given source path.
    """
    with source.open(mode="r") as file:
        data = file.readlines()
    parsed_data = [line.strip().split(delimiter) for line in data]
    print(parsed_data)
    return parsed_data


def parse_csv_to_json(data: list[list[str]]) -> list:
    """Converte lista de dados para formato de lista de dicionario"""
    columns = data[0]
    lines = data[1:]
    result = [dict(zip(columns, line)) for line in lines]
    return result


def write_json_data(data: list[dict[str, str]], output_path: Path):
    """Escreve uma lista de dicionarios em formato json em disco"""
    with output_path.open(mode="w") as file:
        file.write("[\n")
        for d in data[:-1]:
            write_dictionary(d, file, append_comma=True)
        write_dictionary(d, file, append_comma=False)
        file.write("]\n")


def write_dictionary(data: dict, io, append_comma: bool = True):
    """Escreve um dicionario no disco."""
    io.write("\t{\n")
    items = tuple(data.items())
    for line in items:
        write_line(line, io, True)
    write_line(line, io, False)
    io.write("\t}")
    if append_comma:
        io.write(",\n")
    else:
        io.write("\n")


def write_line(line: tuple, io, append_comma: bool = True):
    """Escreve uma linha do dicionario no disco."""
    key, value = line
    if append_comma:
        io.write(f"\t\t{key}: {value},\n")
    else:
        io.write(f"\t\t{key}: {value}\n")
