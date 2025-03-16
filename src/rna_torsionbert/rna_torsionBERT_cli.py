import argparse
from typing import Optional

from rna_torsionbert.helper.rna_torsionBERT_helper import RNATorsionBERTHelper
from rna_torsionbert.utils import read_fasta
from loguru import logger
import torch


class RNATorsionBERTCLI:
    def __init__(
        self,
        in_seq: Optional[str],
        in_fasta: Optional[str],
        out_path: Optional[str],
        device: Optional[str] = "cpu",
        *args,
        **kwargs,
    ):
        self.sequence = self._init_inputs(in_seq, in_fasta)
        self.out_path = out_path
        self.device = torch.device(device)

    def _init_inputs(self, in_seq: Optional[str], in_fasta: Optional[str]) -> str:
        """
        Initialise the inputs given the arguments
        :return: the sequence
        """
        if in_seq is None and in_fasta is None:
            raise ValueError("You must provide either a sequence or a fasta file.")
        if in_seq is not None and in_fasta is not None:
            raise ValueError(
                "Please provide only the sequence or the fasta file, not both."
            )
        if in_seq is not None:
            sequence = in_seq
        elif in_fasta is not None:
            sequence = read_fasta(in_fasta)
        return sequence

    def run(self):
        output = RNATorsionBERTHelper(self.device).predict(self.sequence)
        if self.out_path is not None:
            output.to_csv(self.out_path)
            logger.info(f"Saved the output to {self.out_path}")
        return output

    @staticmethod
    def get_args():
        parser = argparse.ArgumentParser(
            description="Prediction of Torsional angles for RNA structures"
        )
        # Add command line arguments
        parser.add_argument(
            "--in_seq",
            dest="in_seq",
            type=str,
            help="RNA Input sequence.",
            default=None,
        )
        parser.add_argument(
            "--in_fasta",
            dest="in_fasta",
            type=str,
            help="Path to a fasta file.",
            default=None,
        )
        parser.add_argument(
            "--out_path",
            dest="out_path",
            type=str,
            help="Path to a .csv file to save the prediction",
            default=None,
        )
        parser.add_argument(
            "--device",
            dest="device",
            type=str,
            help="Device to use for the prediction. Default is 'cpu'. Selection between 'cpu' and 'cuda'",
            default="cpu",
        )
        # Parse the command line arguments
        args = parser.parse_args()
        return args

def main():
    args = RNATorsionBERTCLI.get_args()
    rna_torsionBERT_cli = RNATorsionBERTCLI(**vars(args))
    rna_torsionBERT_cli.run()


if __name__ == "__main__":
    main()