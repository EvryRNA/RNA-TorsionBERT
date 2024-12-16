run:
	python -m src.rna_torsionBERT_cli --in_seq="ACCCCCGUUUCC" --out_path=data/output/rna_tb_out.csv

run_fasta:
	python -m src.rna_torsionBERT_cli --in_fasta=data/rp02.fasta --out_path=data/output/rna_tb_out_fasta.csv

run_tb_mcq:
	python -m src.tb_mcq_cli --in_pdb=data/preds/3drna_rp11.pdb --out_path=data/output/tb_mcq_out.csv

run_tb_mcq_all:
	python -m src.tb_mcq_cli --in_pdb=data/preds --out_path=data/output/tb_mcq_out_all.csv

docker_run:
	docker build -t rna_torsionbert .
	docker run --rm -it rna_torsionbert