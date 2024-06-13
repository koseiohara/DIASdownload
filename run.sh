#!/bin/bash

YEAR_INI=1978
YEAR_FIN=${YEAR_INI}
SCRIPT=download.py

TYPE=fcst_phyp125
PARAM_LIST="ttswr ttlwr lrghr cnvhr vdfhr"
#PARAM_LIST="ttswr ttlwr lrghr cnvhr"
#PARAM_LIST="vdfhr"

if [ ! -d log ]
then
    mkdir log
fi


function DAYNUM(){
    YEAR_INPUT=$1
    if [ $(expr ${YEAR_INPUT} % 4) != 0 ]
    then
                #     1  2  3  4  5  6  7  8  9 10 11 12
        DAYS_LIST=(0 31 28 31 30 31 30 31 31 30 31 30 31)
    elif [ $(expr ${YEAR_INPUT} % 100) = 0 -a $(expr ${YEAR_INPUT} % 400) != 0 ]
    then
                #     1  2  3  4  5  6  7  8  9 10 11 12
        DAYS_LIST=(0 31 28 31 30 31 30 31 31 30 31 30 31)
    else
                #     1  2  3  4  5  6  7  8  9 10 11 12
        DAYS_LIST=(0 31 29 31 30 31 30 31 31 30 31 30 31)
    fi
}


for YEAR in $(seq ${YEAR_INI} 1 ${YEAR_FIN})
do

    DAYNUM ${YEAR}

    for MONTH in $(seq  1 1 12)
    do
        MM=$(printf "%02d" "${MONTH}")
        for PARAM in ${PARAM_LIST}
        do
            TITLE=${TYPE}"_"${PARAM}
            echo "python2 ${SCRIPT} ${YEAR}/${MM}/01/00 ${YEAR}/${MM}/${DAYS_LIST[${MONTH}]}/18 ${TITLE} &"
            python2 ${SCRIPT} ${YEAR}/${MM}/01/00 ${YEAR}/${MM}/${DAYS_LIST[${MONTH}]}/18 ${TITLE} &
        done

        echo
    done

done

