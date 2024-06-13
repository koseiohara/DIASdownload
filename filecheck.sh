#!/bash/bin

RESULT="existence.txt"

## Number of days in each month (considering leap year)
# Argument : YEAR
function DAYNUM(){
	YEAR_INPUT=$1
	if [ $(expr ${YEAR_INPUT} % 4) != 0 ]
	then
		 	#      1  2  3  4  5  6  7  8  9 10 11 12
		daynum=(0 31 28 31 30 31 30 31 31 30 31 30 31)
	elif [ $(expr ${YEAR_INPUT} % 100) = 0 -a $(expr ${YEAR_INPUT} % 400) != 0 ]
	then
			#      1  2  3  4  5  6  7  8  9 10 11 12
		daynum=(0 31 28 31 30 31 30 31 31 30 31 30 31)
	else
			#      1  2  3  4  5  6  7  8  9 10 11 12
		daynum=(0 31 29 31 30 31 30 31 31 30 31 30 31)
	fi
}

function MONTHLY(){
	MONTH0=$(printf "%02d" "${MONTH}")

    FNAME="${TITLE}.${YEAR}${MONTH0}.ctl"
    FILE_FULL="${DIR}/${YEAR}${MONTH0}/${FNAME}"
	if [ ! -e "${FILE_FULL}" ]
	then
		echo "${FILE_FULL} does not exist" >> "${RESULT}"
	fi

    FNAME="${TITLE}.${YEAR}${MONTH0}.idx"
    FILE_FULL="${DIR}/${YEAR}${MONTH0}/${FNAME}"
	if [ ! -e "${FILE_FULL}" ]
	then
		echo "${FILE_FULL} does not exist" >> "${RESULT}"
	fi

	DAYNUM ${YEAR}

	for DAY in $(seq -w 1 1 ${daynum[MONTH]})
	do
		for HOUR in $(seq -w 0 6 18)
		do
			FNAME="${TITLE}.${YEAR}${MONTH0}${DAY}${HOUR}"
			FILE_FULL="${DIR}/${YEAR}${MONTH0}/${FNAME}"
			# echo "${FILE_FULL}" >> "${RESULT}"
			if [ ! -e "${FILE_FULL}" ]
			then
				echo "${FILE_FULL} does not exist" >> "${RESULT}"
			fi
		done
	done
}


function CHECKER(){
	YEAR_INI=$1
	YEAR_FIN=$2
	DIR="$3"
	TITLE="$4"

	YEAR="${YEAR_INI}"

	printf "%-15s" "${TITLE}  "
	#for MONTH in $(seq 9 1 12)
	#do
	#	MONTHLY
	#done

	echo -n "-"

	#for YEAR in $(seq $(expr ${YEAR_INI} + 1) 1 $(expr ${YEAR_FIN} - 1))
	#for YEAR in $(seq ${YEAR_INI} 1 ${YEAR_FIN})
	for YEAR in $(seq ${YEAR_INI} 1 $(expr ${YEAR_FIN} - 1))
	do
		for MONTH in $(seq 1 1 12)
		do
			MONTHLY
		done
		#echo -n "${YEAR}-"
		echo -n "-"
	done

	YEAR="${YEAR_FIN}"
	for MONTH in $(seq 1 1 5)
	do
		MONTHLY
	done
	echo -n "-"

	echo "  COMPLETE"
}


rm -fv "${RESULT}"

INI=1980
FIN=2024

CHECKER ${INI} ${FIN} "/mnt/jet12/JRA3Q/Daily/fcst_phyp125" "fcst_phyp125_ttswr"
CHECKER ${INI} ${FIN} "/mnt/jet12/JRA3Q/Daily/fcst_phyp125" "fcst_phyp125_ttlwr"
CHECKER ${INI} ${FIN} "/mnt/jet12/JRA3Q/Daily/fcst_phyp125" "fcst_phyp125_cnvhr"
CHECKER ${INI} ${FIN} "/mnt/jet12/JRA3Q/Daily/fcst_phyp125" "fcst_phyp125_vdfhr"
CHECKER ${INI} ${FIN} "/mnt/jet12/JRA3Q/Daily/fcst_phyp125" "fcst_phyp125_lrghr"

#CHECKER "/mnt/jet12/JRA3Q/Daily/anl_p125" "anl_p125_tmp"
#CHECKER "/mnt/jet12/JRA3Q/Daily/anl_p125" "anl_p125_depr"
#CHECKER "/mnt/jet12/JRA3Q/Daily/anl_p125" "anl_p125_spfh"
#CHECKER "/mnt/jet12/JRA3Q/Daily/anl_p125" "anl_p125_rh"
#CHECKER "/mnt/jet12/JRA3Q/Daily/anl_p125" "anl_p125_ugrd"
#CHECKER "/mnt/jet12/JRA3Q/Daily/anl_p125" "anl_p125_vgrd"
#CHECKER "/mnt/jet12/JRA3Q/Daily/anl_p125" "anl_p125_strm"
#CHECKER "/mnt/jet12/JRA3Q/Daily/anl_p125" "anl_p125_vpot"
#CHECKER "/mnt/jet12/JRA3Q/Daily/anl_p125" "anl_p125_vvel"
#CHECKER "/mnt/jet12/JRA3Q/Daily/anl_p125" "anl_p125_relv"
#CHECKER "/mnt/jet12/JRA3Q/Daily/anl_p125" "anl_p125_reld"
#CHECKER "/mnt/jet12/JRA3Q/Daily/anl_p125" "anl_p125_hgt"
#CHECKER "/mnt/jet12/JRA3Q/Daily/anl_surf125" "anl_surf125"

if [ ! -e "${RESULT}" ]
then
	echo "ALL FILES EXIST" >> "${RESULT}"
fi

