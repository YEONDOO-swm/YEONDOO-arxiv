import os
import requests
import re
from bs4 import BeautifulSoup 
import sys
from tqdm import tqdm
from tqdm.contrib.concurrent import process_map  # or thread_map
from multiprocessing import Pool, cpu_count



global yymm
dic={}

def download(cs_file):
    
    prefix="gs://arxiv-dataset/arxiv/arxiv/pdf/"+yymm+"/"
    
    if cs_file in dic.keys():
        src_file_name=prefix+cs_file+'v'+dic[cs_file]+'.pdf'
        dest_file_name=os.path.join('./data',year,month,cs_file+'v'+dic[cs_file])+'.pdf'

        # cmd="gcloud alpha storage cp "+src_file_name+" "+dest_file_name
        cmd="gsutil -m cp "+src_file_name+" "+dest_file_name
        os.system(cmd+" > /dev/null 2>%1")
    


if __name__ == "__main__":

    print("parsing...")
    for nametxt in (os.listdir(os.path.join('./yymmlist',sys.argv[1]))):
        try:
            yymm=nametxt.split('.')[0]
            assert yymm != ""
            year=yymm[:2]
            month=yymm[2:]
            url = f"https://arxiv.org/list/cs.AI/{ yymm }"
            print(url)
            response = requests.get(url)
            
            html = response.text

            total_paper_pattern =  r'total of (\d+) entries'

            soup = BeautifulSoup(html, 'html.parser')
            small_tag = soup.find('small')
            text = small_tag.get_text()
            match = re.search(total_paper_pattern, text)
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            if match:
                number = match.group(1)

            else:
                print("number error")
                exit(0)
        
        
            cs_list=[]
            number = int(number)
            
            for page in tqdm(range(0, number, 2000)):
                url = f"https://arxiv.org/list/cs.AI/{ yymm }?skip={ page }&show={ number }"
                response = requests.get(url)
                html = response.text
                soup = BeautifulSoup(html, 'html.parser')
                items = soup.find_all('a', href=True, title='Abstract')
                for item in items:
                    item = item.text
                    arxiv_number = item.split(':')[1]
                    cs_list.append(arxiv_number)
        except Exception as e:
            print(e)
            continue

        print("downloading...")


        
        file_path = os.path.join('./yymmlist',year)+'/'+nametxt
        with open(file_path) as f:
            yymm_lists = f.read().splitlines()

        dic.clear()
        for yymm_list in yymm_lists:
            file=yymm_list.split('/')[-1]
            id=file[:-6]
            ver=file[-5:-4]
            if not id in dic.keys():
                dic[id]=ver
            else:
                if(dic[id]<ver):
                    dic[id]=ver
        cnt=0
        not_downloaded=[]
        exists_cs_list=[]
        for cs in cs_list:
            if cs not in dic.keys():
                not_downloaded.append(cs)
            else :
                exists_cs_list.append(cs)

        
        num_cpu=cpu_count()
        chunksize=2

        r= process_map(download,exists_cs_list,max_workers=num_cpu,chunksize=chunksize)
        
        file_name=os.path.join('./remain',year,year+month)+'.txt'
        with open(file_name, 'w+') as file:
            file.write('\n'.join(not_downloaded))
        print("the number of papers : ",number," | not downloaded : ",len(not_downloaded))
        
