import argparse
from typing import Optional

from src.rna_torsionBERT_helper import RNATorsionBERTHelper
from src.utils import read_fasta, save_json
from loguru import logger


class RNATorsionBERTCLI:
    def __init__(self, in_seq: Optional[str], in_fasta: Optional[str], out_path: Optional[str], *args, **kwargs):
        self.sequence = self._init_inputs(in_seq, in_fasta)
        self.out_path = out_path

    def _init_inputs(self, in_seq: Optional[str], in_fasta: Optional[str]) -> str:
        """
        Initialise the inputs given the arguments
        :return: the sequence
        """
        if in_seq is None and in_fasta is None:
            raise ValueError("You must provide either a sequence or a fasta file.")
        if in_seq is not None and in_fasta is not None:
            raise ValueError("Please provide only the sequence or the fasta file, not both.")
        if in_seq is not None:
            sequence = in_seq
        elif in_fasta is not None:
            sequence = read_fasta(in_fasta)
        return sequence


    def run(self):
        output = RNATorsionBERTHelper().predict(self.sequence)
        if self.out_path is not None:
            save_json(output, self.out_path)
            logger.info(f"Saved the output to {self.out_path}")
        return output

    @staticmethod
    def get_args():
        parser = argparse.ArgumentParser(description="Prediction of Torsional angles for RNA structures")
        # Add command line arguments
        parser.add_argument("--in_seq", dest="in_seq" ,type=str, help="RNA Input sequence.", default=None)
        parser.add_argument("--in_fasta", dest = "in_fasta", type=str, help="Path to a fasta file.", default=None)
        parser.add_argument("--out_path", dest="out_path", type=str, help="Path to a .json file to save the prediction", default=None)
        # Parse the command line arguments
        args = parser.parse_args()
        return args


if __name__ == "__main__":
    args = RNATorsionBERTCLI.get_args()
    rna_torsionBERT_cli = RNATorsionBERTCLI(**vars(args))
    rna_torsionBERT_cli.run()
