# years="14 15 16 17 18 19 20 21 22"
years="23"
# years=$1
# months="01 02 03 04 05 06 07 08 09 10 11 12"
months="07"
mkdir ./data
mkdir ./yymmlist
mkdir ./remain
for year in $years
do
	echo $year "start"
 	
	mkdir ./yymmlist/$year
    mkdir ./remain/$year
    mkdir ./data/$year
	for month in $months
        
        do
            if [ ! -f ./yymmlist/$year/$year$month.txt ]; then
                echo "txt is not exists"
                gsutil list gs://arxiv-dataset/arxiv/arxiv/pdf/$year$month/ > ./yymmlist/$year/$year$month.txt
                echo $month "done"
            else
                echo "txt is already exists"
            fi
                mkdir ./data/$year/$month
	done
	# python3 main.py $1
    python3 main.py $year
    for month in $months
        do
            ls ./data/$year/$month > ./data/$year/$month/filelist.txt
	done
done
