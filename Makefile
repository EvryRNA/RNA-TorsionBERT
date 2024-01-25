run:
	python -m src.rna_torsionBERT_cli --in_seq="ACCCCCGUUUCC" --out_path=data/out.json

run_fasta:
	python -m src.rna_torsionBERT_cli --in_fasta=data/rp02.fasta --out_path=data/out_fasta.json