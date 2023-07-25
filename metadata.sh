#!/bin/bash

# years="14 15 16 17 18 19 20 21 22"
years="23"
# years=$1
# months="01 02 03 04 05 06 07 08 09 10 11 12"
months="07"

mkdir ./meta

for year in $years
do
    mkdir ./meta/$year
    # 파일 경로를 지정합니다.
    for month in $months
    do
        mkdir ./meta/$year/$month
        file_path="./data/$year/$month/filelist.txt"  # 여기에 실제 파일 경로를 입력하세요.

        # 파일을 읽어 리스트로 만듭니다.
        read_file_to_list() {
            if [ -f "$1" ]; then
                # 파일을 줄 단위로 읽어서 배열로 저장합니다.
                IFS=$'\n' read -d '' -r -a file_content_list < "$1"
            else
                echo "Error: file not founded."
                exit 1
            fi
        }

        # 함수를 호출하여 파일을 읽어 리스트를 만듭니다.
        read_file_to_list "$file_path"

        # 리스트를 순회하며 각 요소를 출력하는 예시 for문
        cnt=0
        start_time=$(date +%s)
        for item in "${file_content_list[@]}"; do
            ((cnt++))
            end_time=$(date +%s)
            duration=$((end_time - start_time))
            echo -ne "Downloading file $cnt of ${#file_content_list[@]}  $(($duration / 60)) minutes and $(($duration % 60))secs\r"
            
            wget http://export.arxiv.org/api/query?id_list=${item:0:12} --output-document=./meta/$year/$month/${item:0:12}.xml > /dev/null 2>%1
        done
    done
done
