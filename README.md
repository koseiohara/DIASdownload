# Script for Downloading Data from DIAS
The script is based on the one distributed by DIAS, with modifications applied

## Environment
CentOS7  
Python2.7.5


## Setting
1. Set the periods for the data to be downloaded  
    Rewrite the definitions of `INITIAL_DATE` and `FINAL_DATE`.
    Their arguments are year, month, day, and hour, respectively.

1. Set the temporal resolution  
    Rewrite the definition of `DATA_HOUR_DELTA`.
    If you download 6-hourly data, `DATA_HOUR_DELTA=6`.
    For example, if daily, `DATA_HOUR_DELTA=24`.

1. Set the number of download attempts for each data  
    Rewrite the definition of `TRY_MAX`.
    If download is failed, downloading is tried again `TRY_MAX` times.
    1-5 is recommended.

1. Set the directory of data  
    Rewrite the definition of `DIAS_DIRECTORY`.
    Note that this directory is not for your computer, but for DIAS.
    Open DIAS Download Website and check the path.
    For example, "`/JRA3Q/Hist/Daily/anl_p125/`" for JRA3Q 6-hourly `anl_p125` dataset.
    "`/JRA3Q/Hist/Daily/anl_p125`" is also available because "`/`" is padded if the last character is not "`/`".

1. Set the title of data  
    Rewrite the definition of `TITLE`.
    "`anl_p125_ugrd`" for u-wind on isobaric surfaces of JRA3Q 6-hourly analysis data and
    "`fcst_phyp125_ttswr`" for temperature tendency due to short wave radiation of JRA3Q 6-hourly forecast data.

1. Set the destination directory for data  
    Rewrite the definition of `COMP_DIRECTORY`.
    This is a directory of your computer.
    Data is downloaded under there.
    Like `DIAS_DIRECTORY`, the last character do not have to "`/`".

1. Set the dataset number  
    Rewrite the definition of `targeturl`.
    Access DIAS Download Website and check its URL to find the dataset number.
    645 for JRA3Q and targeturl is defined as "https://data.diasjp.net/dl/storages/filelist/dataset:645".

1. Others  
    If the format of file name or dias-directory is not suit for your data, 
    edit `get_filename_data`, `get_filename_grads`, `get_dias_directory`, and `get_computer_directory`.
    `get_filename_data` defines the file name of data.
    `get_filename_grads` defines the file name of control and index files.
    `get_dias_directory` defines the directory of dias.
    `get_computer_directory` defines the destination directory for downloaded data.


## Run
Command to run the script:
```sh
$ python2 download.py
```
You will be prompted to enter your username and password.
Username is your e-mail adress to login DIAS

### Command Line Argument
command line arguments can be defined.
Here is the example:
```sh
$ python2 download.py 2022/03/01/00 2022/03/31/18 fcst_phyp125_ttlwr
```
The first and second command line arguments are for `INITIAL_DATE` and `FINAL_DATE`, respectively.
Their format is "`YYYY/MM/DD/HH`".
The third one is for `TITLE`.
If the format of the first and second are invalid or one of the command line arguments are missing, 
their parameters are defined by the values written in the script.


## Account Authentication
If `./account.txt` exists, your username and password are read from the file.
Write your username in the first line and password in the second line.
For security reasons, change the permission of account.txt so as not to be read your information by others.


## Log
`./log/` is needed.
In the log file, the setting is recorded at first, then the results of downloading is written.
The format of downloading result is:  
    YYYY/MM/DD HH:MM:SS  (ABSOLUTE PATH OF FILE) EXIST/OK/NG  
The first block is the date and time which the downloading is executed.
If the last word is EXIST, the file has existed and the download command is not executed.
If OK, file was downloaded correctory.
If NG, download was failed.


