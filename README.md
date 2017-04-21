# Running Epimobile using Docker (easier if you have Docker installed)

After you've installed docker, run:

1. `docker build -t epimobile:latest .`

2. `docker volume create --name dbdata`

3. `docker run -v dbdata:/var/lib/postgresql -p 5000:5000 epimobile`

If you want to run /bin/bash *inside* the container:

`docker run -i -t --rm epimobile /bin/bash`


# Running Epimobile without using Docker

1. Make sure you have all the dependencies by checking the `requirements.txt` and `Dockerfile`

2. Run the script `init_database.py` in the database folder (make sure you have postgresql installed)

3. run `app.py`


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

# Current features

- Complete end-to-end system to analyze blood sample and find pathogens

- Analyzis can be performed by using a simple web UI

- Although the UI is web based, no internet connection is required, it will be running on local host

- All data and all mash output is stored in an easy to use database


# Future

- Finish communication module: allow local devices to share their analyzes (halfway finished) and allow global shared with remote server

