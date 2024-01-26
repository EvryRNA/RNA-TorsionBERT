# RNA-TorsionBERT

`RNA-TorsionBERT` is a 331 MB parameter BERT-based language model that predicts RNA torsional and pseudo-torsional angles from the sequence.

![](./img/dnabert_architecture_final.drawio.png)


`RNA-TorsionBERT` is a DNABERT model that was pre-trained on ~4200 RNA structures before being fine-tuned on 185 non-redundant structures from rsRNASP.

It provides an improvement of MAE of 6.2° over the previous state-of-the-art model, SPOT-RNA-1D, on the Test Set (composed of RNA-Puzzles and CASP-RNA).

| Model  | $\alpha$ | $\beta$  | $\gamma$  | $\delta$  | $\epsilon$  | $\zeta$  | $\chi$  | $\eta$  | $\theta$  | 
|------------------|----------|------|------|------|------|------|------|------|------| 
| **RNA-TorsionBERT**  | 37.3     | 19.6 | 29.4 | 13.6 | 16.6 | 26.6 | 14.7 | 20.1 | 25.4 | 
| SPOT-RNA-1D        | 45.7     | 23   | 33.6 | 19   | 21.1 | 34.4 | 19.3 | 28.9 | 33.9 | 

## Installation

To install RNA-TorsionBERT and it's dependencies following commands can be used in terminal:

```bash
pip install -r requirements.txt 
```


## Usage

To run the RNA-TorsionBERT, you can use the following command line:
```bash
python -m src.rna_torsionBERT_cli [--seq_file] [--in_fasta] [--out_path]
```

The arguments are the following:
- `--seq_file`: RNA Sequence. 
- `--in_fasta`: Path to the input sequence fasta file. 
- `--out_path`: Path to a `.json` file where the output will be saved. 

You can also import in your python code the class `RNATorsionBERTCLI` from `src.rna_torsionBERT_cli`. 

To run the code using `Docker`, you can use the following command line:
```bash
docker build -t rna_torsionbert .
docker run -it rna_torsionbert 
```

It will enter into a bash console where you could execute the previous commands with all the installations done. 

To have example of commands, you can look at the `Makefile`.


## Citation

TO BE COMPLETED