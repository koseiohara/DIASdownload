# Script for Downloading Data from DIAS
This script is based on the one distributed by DIAS, with modifications applied

## Test Environment
- CentOS 7
- Python 2.7.5


## Setting
1. Set the period of data to be downloaded  
    Modify the definitions of `INITIAL_DATE` and `FINAL_DATE`.
    Their arguments are year, month, day, and hour, respectively.

1. Set the temporal resolution  
    Rewrite the definition of `DATA_HOUR_DELTA`.
    If you download 6-hourly data, `DATA_HOUR_DELTA=6`.
    For example, if daily, `DATA_HOUR_DELTA=24`.

1. Set the number of download attempts per dataset  
    Modify the definition of `TRY_MAX`.
    If a download failed, it will be retried up to `TRY_MAX` times.
    A value between 1 and 5 is recommended.

1. Set the DIAS directory  
    Modify the definition of `DIAS_DIRECTORY`.
    Note that this directory refers to DIAS, not your local computer.
    Open DIAS Download Website and check the dataset path.
    For example, "`/JRA3Q/Hist/Daily/anl_p125/`" for the JRA-3Q 6-hourly `anl_p125` dataset.
    "`/JRA3Q/Hist/Daily/anl_p125`" is also valid, since "`/`" will be automatically appended if missing.

1. Set the title of data  
    Modify the definition of `TITLE`.  
    For example:
    - `"anl_p125_ugrd"` for u-wind on isobaric surfaces of JRA-3Q 6-hourly analysis data
    - `"fcst_phyp125_ttswr"` for temperature tendency due to short wave radiation of JRA-3Q 6-hourly forecast data.

1. Set the destination directory on your computer  
    Modify the definition of `COMP_DIRECTORY`.
    Data will be downloaded under this directory.
    As with `DIAS_DIRECTORY`, the trailing "`/`" is optional.

1. Set the dataset number  
    Modify the definition of `targeturl`.
    Visit the DIAS Download Website and check its URL to find the dataset number.  
    For example, JRA-3Q correspond to `645`, so:
    ```python
    targeturl = "https://data.diasjp.net/dl/storages/filelist/dataset:645"
    ```

1. Other customizations  
    If the filename or directory structure differs for your dataset, edit the following functions:
    - `get_filename_data`: defines the data filename.
    - `get_filename_grads`: defines filenames of control and index files.
    - `get_dias_directory`: defines the DIAS directory.
    - `get_computer_directory`: defines the destination directory on your computer.


## Run
To execute the script:
```sh
$ python2 download.py
```
You will be prompted to enter your username and password.
Username is your e-mail address used to log in to DIAS.

### Command Line Argument
command line arguments can also be used.  
Example:
```sh
$ python2 download.py 2022/03/01/00 2022/03/31/18 fcst_phyp125_ttlwr
```
The first and second command line arguments correspond to `INITIAL_DATE` and `FINAL_DATE`.
Their format is "`YYYY/MM/DD/HH`".
The third specifies `TITLE`.
If the first and second arguments are invalid, or if arguments are missing, the script will instead use the values defined within it.


## Account Authentication
If `./account.txt` exists, your username and password are read from the file.
- First line: username  
- Second line: password  
For security reasons, change the file permissions of `account.txt` so that others cannot read your credentials.


## Log
`./log/` is required.
Each log file records the settings first, followed by the download results.  
The format of the result is:  
```txt
YYYY/MM/DD HH:MM:SS  (ABSOLUTE PATH OF FILE) EXIST/OK/NG  
```
The first block is the date and time of the download execution.
If the last word is `EXIST`, the file already exists and the download command was skipped
If `OK`, the file was downloaded successfully.
If `NG`, the download failed.


