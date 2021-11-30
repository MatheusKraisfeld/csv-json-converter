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
    save_to_json_files(csvs=data, output_path=output_path, prefix=prefix)


def read_csv_file(source: Path, delimiter: str = ",") -> tuple:
    """Load a single csv file or all files withing a directory.

    Args:
        source (Path): Path for a single file or directory with files.
        delimiter (str, optional): Separator columns in the csv's. Defaults to ",".

    Returns:
        tuple: All dataframes loaded from the given source path.
    """
    if source.is_file():
        logger.info("Reading csv file %s", source)
        return (pd.read_csv(source, delimiter=delimiter, index_col=False),)

    logger.info("Reading all files within the directory: %s", source)
    data = list()
    for i in source.iterdir():
        data.append(pd.read_csv(file_path_or_buffer=i, delimiter=delimiter, index_col=False))

    return tuple(data)


def save_to_json_files(csvs: tuple, output_path: Path, prefix: str = None):
    """Save dataframes to disk.

    Args:
        csvs (tuple): Tuple with dataframes that will be converted.
        output_path (Path): Path where to save the json files.
        prefix (str, optional): Name to prepend to files. If nothing is given it will use `file_`. Defaults to None.
    """
    i = 0
    while i < len(csvs):
        file_name = f"{prefix}_{i}.json"
        output = output_path.joinpath(file_name)
        logger.info("Saving file: %s", output)
        data: pd.DataFrame = csvs[i]
        data.to_json(path_or_buf=output, orient="records", indent=4)
        i += 1
