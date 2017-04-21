# About Epimobile

Rapid identification of disease causing infectious agents (pathogens) in patients is important to enable rapid responses to potential, or ongoing, outbreaks. New advances in genomic sequencing technologies are enabling more effective point-of-care diagnosis -- where patient samples can be analyzed for the detection of pathogen DNA. However, it has yet to be understood how these technologies can be applied in the field and under resource constraints that hinder cloud access for computation. Here we present EpiMobile, a conceptual model and minimal viable product (MVP) implementation of a genomics point-of-care workflow using mobile devices. EpiMobile enables analyses of genomic data harvested by a portable genome sequencer and the distribution of the results to local clinical or healthcare teams as well as national, or global, public health agencies, whilst considering computational processing and Internet connectivity resource constraints. Our evaluation of EpiMobile indicates that it has a minimal resource consumption footprint and is accurate when run of a dataset with known outcomes. However, we emphasize that the conceptual and exploratory nature of our work affects to what extent our results would map to real world settings. We discuss the utility of EpiMobile through a set of usage scenarios currently supported by our MVP implementation. We believe that our work provides an interesting overview of an exciting and emerging application contexts as well as proposing an interesting implementation of genomics point-of-care. 

# Running Epimobile using Docker (easier if you have Docker installed)

If you don't want to build the image from scratch (since it could take a while), you can just pull the final docker image and run it:

1. `docker pull digorithm/epimobile`

2. `docker volume create --name dbdata`

3. `docker run -v dbdata:/var/lib/postgresql -p 5000:5000 epimobile`


Or if you want to build the image from scratch, run:

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

