#!/bin/bash

YEAR=2024
MONTH_INI=1
MONTH_FIN=5
SCRIPT=download.py

TYPE=fcst_phyp125
PARAM_LIST="ttswr ttlwr lrghr cnvhr vdfhr"

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


DAYNUM ${YEAR}

for MONTH in $(seq  ${MONTH_INI} 1 ${MONTH_FIN})
do
    MM=$(printf "%02d" "${MONTH}")
    for PARAM in ${PARAM_LIST}
    do
        TITLE=${TYPE}"_"${PARAM}
        echo "python2 ${SCRIPT} "${YEAR}/${MM}/01/00" "${YEAR}/${MM}/${DAYS_LIST[${MONTH}]}/18" ${TITLE} &"
        python2 ${SCRIPT} "${YEAR}/${MM}/01/00" "${YEAR}/${MM}/${DAYS_LIST[${MONTH}]}/18" ${TITLE} &
    done

    echo
done


