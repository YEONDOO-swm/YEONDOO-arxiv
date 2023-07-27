years="14 15 16 17 18 19 20 21 22 23"
# years="14"
# years=$1
months="01 02 03 04 05 06 07 08 09 10 11 12"
# months="01"
mkdir ./meta
for year in $years
do
	echo $year "start"

    mkdir ./meta/$year
	for month in $months 
        do
            mkdir ./meta/$year/$month
            python3 meta.py $year $month
	    done
done
