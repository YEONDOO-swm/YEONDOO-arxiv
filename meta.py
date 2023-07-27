import fitz
import arxiv
import os,sys
from tqdm.contrib.concurrent import process_map  # or thread_map
from multiprocessing import Pool, cpu_count


basedir="/home/soma4/YEONDOO-arxiv-with-version/YEONDOO-arxiv/data/"
year = sys.argv[1]
month = sys.argv[2]
path_data=os.path.join(basedir,year,month)
id_list=os.listdir(path_data)

id_list=[id.split('.pdf')[0] for id in os.listdir(path_data)]



def get_meta(id):
    outdir=os.path.join("./meta",year,month,str(id))+".xml"
    cmd="wget http://export.arxiv.org/api/query?id_list="+str(id)+" --output-document="+outdir
    os.system(cmd+" > /dev/null 2>%2")

if __name__ == "__main__":
    num_cpu=cpu_count()
    chunksize=2

    r= process_map(get_meta,id_list,max_workers=num_cpu,chunksize=chunksize)