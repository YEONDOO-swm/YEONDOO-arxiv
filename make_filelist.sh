years="14 15 16 17 18 19 20 21 22 23"
# years="23"
# years=$1
months="01 02 03 04 05 06 07 08 09 10 11 12"
for year in $years
    do
        for month in $months
            do
                ls ./data/$year/$month > ./data/$year/$month/filelist.txt
            done
    done