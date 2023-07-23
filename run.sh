#years="20 21 22 23"
years=$1
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
	for month in $months
        do
            if [ ! -f ./yymmlist/$year/$year$month.txt ]; then
                echo "txt is not exists"
                gsutil list gs://arxiv-dataset/arxiv/arxiv/pdf/$year$month/ > ./yymmlist/$year/$year$month.txt
                echo $month "done"
            fi
                echo "txt is already exists"
	done
	python3 main.py $1
done
