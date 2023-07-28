import json
import fitz
import pandas as pd
import os
from langchain.docstore.document import Document
from tqdm import tqdm
from tqdm.contrib.concurrent import process_map  # or thread_map
from multiprocessing import cpu_count

from multiprocessing import Manager
from functools import partial
import gc

import tiktoken

from langchain.text_splitter import RecursiveCharacterTextSplitter
import sys

from concurrent.futures import ProcessPoolExecutor
from langchain.vectorstores import OpenSearchVectorSearch
from langchain.embeddings import OpenAIEmbeddings

from langchain.text_splitter import TokenTextSplitter
import time
# Get a list of dicts and convert into a pandas df.
arxiv_data = []
for line in open('../arxiv-metadata-oai-snapshot.json', 'r'):
    arxiv_data.append(json.loads(line))
df = pd.DataFrame.from_records(arxiv_data)
df_filtered = df[df['categories'].str.contains('cs', na=False)]

del arxiv_data
gc.collect()
# del df
# gc.collect()

embeddings = OpenAIEmbeddings()


encoding = tiktoken.encoding_for_model("text-embedding-ada-002")


os.environ['OPENAI_API_KEY']="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"
def Wrapper(shared_list,doc_file_name):
    
    id=doc_file_name.split('v')[0]
    file_path=os.path.join(basedir,year,month,doc_file_name)
    try:
        with fitz.open(file_path) as doc_file:
            text: str = "".join(page.get_text() for page in doc_file)
    except:
        # print(file_path)
        return
    result=df_filtered[df_filtered["id"]==id]
    if result.empty:
        result=df[df["id"]==id]
    if result.empty:
        print("meta not founded : ",id)
        return
    metadata = {
        "Published": str(result["update_date"].item()),
        "Title": result.title.item(),
        "Authors": result.authors.item().replace('and',',').split(','),
        "Summary": result.abstract.item(),

        "paper_id": id,

        "journal_ref": result['journal-ref'].item(),
        
        "categories": result.categories.item().split(' '),
        "source": "http://arxiv.org/abs/"+id,
    }
    doc = Document(
        page_content=text, metadata=metadata
    )
    shared_list.append(doc)

def num_tokens_from_doc(shared_list2,doc) -> int:
    """Returns the number of tokens in a text string."""
    string=doc.page_content
    num_tokens = len(encoding.encode(string, allowed_special={"<|endoftext|>"}))
    shared_list2.append(num_tokens)



if __name__ == "__main__":
    basedir="/home/soma4/YEONDOO-arxiv-with-version/YEONDOO-arxiv/data/"
    # years=["14","15","16","17","18","19","20","21","22","23"]
    # years=["16"]
    years=["14"]
    months=["01","02","03","04","05","06","07","08","09","10","11","12"]
    # months=["06","07","08","09","10","11","12"]
    for year in (years):
        print(year)
        for month in months:
            print(month)
            path_data=os.path.join(basedir,year,month)
            pdf_list=os.listdir(path_data)

            chunksize=2

            manager = Manager()
            shared_list = manager.list()
            process_map(partial(Wrapper, shared_list),pdf_list,max_workers=5,chunksize=chunksize)

            # text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
            text_splitter = TokenTextSplitter(model_name="text-embedding-ada-002",allowed_special={"<|endoftext|>"},chunk_size=250, chunk_overlap=0)
            texts = text_splitter.split_documents(list(shared_list))

            r=len(texts) // 4000
            len_texts=len(texts)

            splitted_texts=[]
            for i in range(r+1):
                start=i*4000
                end=start+4000
                if end>len_texts:
                    end=len_texts
                splitted_texts.append(texts[start:end])
            for splitted_text in tqdm(splitted_texts):

                docsearch = OpenSearchVectorSearch.from_documents(
                    splitted_text,
                    embeddings,
                    opensearch_url="https://search-yeondoo-opensearch-2r3sj6ok7iowthxkgjrnhxsyv4.ap-northeast-2.es.amazonaws.com",
                    http_auth=("admin", "qiQduz-pyrhab-hexzo4"),
                    use_ssl = False,
                    verify_certs = False,
                    ssl_assert_hostname = False,
                    ssl_show_warn = False,
                    index_name="arxiv_test",# with metadata source
                    bulk_size=2000
                )
                time.sleep(60)
            # manager2 = Manager()
            # shared_list2 = manager2.list()
            # # process_map(partial(num_tokens_from_doc, shared_list2),texts,max_workers=5,chunksize=chunksize)
            # with ProcessPoolExecutor(max_workers=5) as executor:
            #     executor.map(partial(num_tokens_from_doc, shared_list2), texts, chunksize=chunksize)
            
            # cnt = sum(shared_list2)
            # price=(cnt/1000)*0.0001
            # file_name=os.path.join('./',"TokenPrice")+'.txt'
            # with open(file_name, 'a') as file:
            #     data = "%lf\n" %(price)
            #     file.write(data)
    
