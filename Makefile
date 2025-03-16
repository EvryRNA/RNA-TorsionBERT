run:
	uv run rna_torsionbert --in_seq="ACCCCCGUUUCC" --out_path=data/output/rna_tb_out.csv --device=cpu

run_fasta:
	uv run rna_torsionbert --in_fasta=data/rp02.fasta --out_path=data/output/rna_tb_out_fasta.csv --device=cpu

run_tb_mcq:
	uv run tb_mcq --in_pdb=data/preds/3drna_rp11.pdb --out_path=data/output/tb_mcq_out.csv --device=cpu

run_tb_mcq_all:
	uv run tb_mcq --in_pdb=data/preds --out_path=data/output/tb_mcq_out_all.csv --device=cuda

docker_run:
	docker build -t rna_torsionbert .
	docker run --rm -it rna_torsionbert