from bioinfo.mash import Mash

mash = Mash()
mash.set_reference_db("data/RefSeqSketches.msh")
mash.run_mash("data/ebov/004674.2D.fastq.gz")

