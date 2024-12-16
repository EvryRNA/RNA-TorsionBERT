import argparse
import os

from loguru import logger
import tqdm
import pandas as pd
from typing import Optional, List

from src.helper.extractor_helper import ExtractorHelper
from src.helper.rna_torsionBERT_helper import RNATorsionBERTHelper
from src.metrics.mcq import MCQ


class TBMCQCLI:
    def __init__(self, in_pdb: str, out_path: Optional[str], *args, **kwargs):
        self.list_files = self._init_pdb(in_pdb)
        self.out_path = out_path

    def _init_pdb(self, in_pdb: Optional[str]) -> List:
        """
        Initialise the inputs structures.
        :param in_pdb: a path to either a .pdb file or a directory of .pdb files
        :return: a list of path to .pdb files
        """
        if os.path.isdir(in_pdb):
            list_files = os.listdir(in_pdb)
            list_files = [os.path.join(in_pdb, file_) for file_ in list_files]
        elif os.path.isfile(in_pdb):
            list_files = [in_pdb]
        else:
            logger.info(f"NO INPUTS FOUND FOR INPUT .PDB: {in_pdb}")
        return list_files

    def run(self):
        all_scores = {"RNA": [], "TB-MCQ": []}
        for in_path in tqdm.tqdm(self.list_files):
            score = self.compute_tb_mcq(in_path)
            all_scores["RNA"].append(os.path.basename(in_path))
            all_scores["TB-MCQ"].append(score)
        all_scores = pd.DataFrame(all_scores, columns=["TB-MCQ", "RNA"]).set_index(
            "RNA"
        )
        if self.out_path is not None:
            logger.info(f"Saved the output to {self.out_path}")
            all_scores.to_csv(self.out_path, index=True)
        return all_scores

    def compute_tb_mcq(self, pred_path: str) -> float:
        """
        Compute the TB-MCQ with RNA-TorsionBERT model
        :param pred_path: the path to the .pdb file of a prediction.
                It could be a native or a predicted structure.
        """
        experimental_angles = ExtractorHelper().extract_all(pred_path)
        sequence = "".join(experimental_angles["sequence"].values)
        torsionBERT_helper = RNATorsionBERTHelper()
        torsionBERT_output = torsionBERT_helper.predict(sequence)
        mcq = MCQ().compute_mcq(experimental_angles, torsionBERT_output)
        return mcq

    @staticmethod
    def get_args():
        parser = argparse.ArgumentParser(
            description="Prediction of Torsional angles for RNA structures"
        )
        # Add command line arguments
        parser.add_argument(
            "--in_pdb",
            dest="in_pdb",
            type=str,
            help="Path a .pdb file or a directory of .pdb files.",
            default=None,
        )
        parser.add_argument(
            "--out_path",
            dest="out_path",
            type=str,
            help="Path to a .csv file to save the predictions.",
            default=None,
        )
        # Parse the command line arguments
        args = parser.parse_args()
        return args


if __name__ == "__main__":
    args = TBMCQCLI.get_args()
    tb_mcq_cli = TBMCQCLI(**vars(args))
    tb_mcq_cli.run()
