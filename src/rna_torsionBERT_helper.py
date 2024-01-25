import transformers
from transformers import AutoModel, AutoTokenizer
import numpy as np
from typing import Optional, Dict

transformers.logging.set_verbosity_error()


ANGLES_ORDER = [
    "alpha",
    "beta",
    "gamma",
    "delta",
    "epsilon",
    "zeta",
    "chi",
    "eta",
    "theta",
]


class RNATorsionBERTHelper:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained(
            "sayby/rna_torsionbert", trust_remote_code=True
        )
        self.params_tokenizer = {
            "return_tensors": "pt",
            "padding": "max_length",
            "max_length": 512,
            "truncation": True,
        }
        self.model = AutoModel.from_pretrained(
            "sayby/rna_torsionbert", trust_remote_code=True
        )

    def predict(self, sequence: str):
        sequence_tok = self.convert_raw_sequence_to_k_mers(sequence)
        inputs = self.tokenizer(sequence_tok, **self.params_tokenizer)
        outputs = self.model(inputs)["logits"]
        outputs = self.convert_sin_cos_to_angles(
            outputs.cpu().detach().numpy(), inputs["input_ids"]
        )
        output_angles = self.convert_logits_to_dict(
            outputs[0, :], inputs["input_ids"][0, :].cpu().detach().numpy()
        )
        return output_angles

    def convert_raw_sequence_to_k_mers(self, sequence: str, k_mers: int = 3):
        """
        Convert a raw RNA sequence into sequence readable for the tokenizer.
        It converts the sequence into k-mers, and replace U by T
        :return: input readable by the tokenizer
        """
        sequence = sequence.upper().replace("U", "T")
        k_mers_sequence = [sequence[i : i + k_mers] for i in range(len(sequence))]
        return " ".join(k_mers_sequence)

    def convert_sin_cos_to_angles(
        self, output: np.ndarray, input_ids: Optional[np.ndarray] = None
    ):
        """
        Convert the raw predictions of the RNA-TorsionBERT into angles.
        It converts the cos and sinus into angles using:
            alpha = arctan(sin(alpha)/cos(alpha))
        :param output: Dictionary with the predictions of the RNA-TorsionBERT per angle
        :param input_ids: the input_ids of the RNA-TorsionBERT. It allows to only select the of the sequence,
            and not the special tokens.
        :return: a np.ndarray with the angles for the sequence
        """
        if input_ids is not None:
            output[
                (input_ids == 0)
                | (input_ids == 2)
                | (input_ids == 3)
                | (input_ids == 4)
            ] = np.nan
        pair_indexes, impair_indexes = np.arange(0, output.shape[-1], 2), np.arange(
            1, output.shape[-1], 2
        )
        sin, cos = output[:, :, impair_indexes], output[:, :, pair_indexes]
        tan = np.arctan2(sin, cos)
        angles = np.degrees(tan)
        return angles

    def convert_logits_to_dict(self, output: np.ndarray, input_ids: np.ndarray) -> Dict:
        """
        Convert the raw predictions into dictionary format.
        It removes the special tokens and only keeps the predictions for the sequence.
        :param output: predictions from the models in angles
        :param input_ids: input ids from the tokenizer
        :return: a dictionary with the predictions for each angle
        """
        index_start, index_end = (
            np.where(input_ids == 2)[0][0],
            np.where(input_ids == 3)[0][0],
        )
        output_angles = {}
        for angle_index, angle in enumerate(ANGLES_ORDER):
            angles = output[index_start + 1 : index_end, angle_index].tolist()
            output_angles[angle] = [round(angle, 2) for angle in angles]
        return output_angles
