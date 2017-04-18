# Testing the bioinformatics module

Before everything: run script `init_database.py` from `scripts` folder

- From root folder, launch `python` from the command line

- `from src.bioinfo.mash import Mash`

- `mash = Mash()`

- `mash.set_reference_db("src/bioinfo/data/RefSeqSketches.msh")`

- `mash.run_mash("src/bioinfo/data/ebov/004674.2D.fastq.gz")`

This should output:

```
Sketching bioinfo/data/ebov/004674.2D.fastq.gz...
Estimated genome size: 333341
Estimated coverage:    7.515
Writing to bioinfo/data/ebov/004674.2D.fastq.gz.msh...
Total hits: 10
['Zaire_ebolavirus', 'Streptococcus_sp._SK643', 'GCF_000085865.1-.-Mycoplasma_hominis_ATCC_23114', 'GCF_000513295.1-.-Magnetospirillum_gryphiswaldense_MSR_1_v2', 'Pasteurella_multocida_subsp._multocida_str._Pm70', 'Scheffersomyces_stipitis_CBS_6054', 'GCF_000319185.1-.-Brachyspira_pilosicoli_WesB', 'Brachyspira_pilosicoli_B2904', 'pRmeGR4b-Sinorhizobium_meliloti_GR4', 'Campylobacter_hominis_ATCC_BAA_381']
```

And your PostgreSQL instance must be populated with the mash output for this DNA Sample.


## Running Epimobile using Docker 

After you've installed docker, run:

1. `docker build -t epimobile:latest .`

2. `docker volume create --name dbdata`

3. `docker run -v dbdata:/var/lib/postgresql -p 5000:5000 epimobile`

If you want to run /bin/bash *inside* the container:

`docker run -i -t --rm epimobile /bin/bash`
