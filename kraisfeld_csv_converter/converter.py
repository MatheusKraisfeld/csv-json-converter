import logging

from pathlib import Path

import click

import pandas as pd

logging.basicConfig(
    level="DEBUG", format="'%(asctime)s - %(name)s - %(levelname)s - %(message)s'"
)
logger = logging.getLogger(__name__)

@click.command()
@click.option("--input", "-i", default="./", help="Path where to find CSV files to be converted to JSON.", type=str)
def converter():
    '''todo'''
    