
# DataSet Distribution Service Indexer (DSDS-Indexer)

This project attempts to index datasets internal to EMBL-EBI based on OmicsDI dataset entries.

The process is mentioned below taking expression-atlas as an example. This will repeat for each of dataset groups,

1. First, the datasets are pulled from omicsDI by dataset where arrayexpress is an example'',

    `python  scripts/extract-omicsdi-datasets.py  arrayexpress`
2. The above script generates CSV which contains dataset file list along with its storage path in EBI internal storage like below,
	
	`/ebi/ftp/pub/databases/arrayexpress/data/experiment/MEXP/E-MEXP-3732`
3. These CSV files are then fed into batch processing on LSF cluster where files are already mounted. The script which does the indexing process is,

    `./1-process-bundle-local.sh eva.csv`
4. The batch process generates list of files along with its checksums (crc32c,md5,blake2b etc.) and locations in EBI (ftp,sftp,globus etc.). These files are further processed so that it is structured like RDSDS data structure so that it can be fed easily into the application. In the end it generates files like,
	- objects.csv
	- access_methods.csv
	- checksums.csv
	- contents.csv


This work is co-funded by the EOSC-hub project (Horizon 2020) under Grant number 777536.