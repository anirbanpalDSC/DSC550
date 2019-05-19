# -*- coding: utf-8 -*-
"""
Spyder Editor
"""

from multiprocessing import Pool
import os, time, json
#from functools import reduce
#from timeit import default_timer as timer
#import pandas as pd

directory = 'C:/Users/Anirban/Desktop/Masters/MSDSC/DSC550/Excercise/data/wikipedia/featured-articles-excercise10.2/'

#jsonl_file_paths = [
#        entry.path
#        for entry in os.scandir(directory.replace("/", "\\")) if entry.name.endswith('.jsonl')
#    ]

json_files = [pos_json for pos_json in os.listdir(directory) if pos_json.endswith('.jsonl')]
type(json_files)

def read_article_jsonl(x):
    records = []
    for i in json_files:
        with open(i,'r') as fi:
            for line in fi:
               records.append(json.loads(line))
    
    return records

if __name__ == '__main__':
    n_processes = [1,2,4,8,16]
    for i in n_processes:
        with Pool(i) as pool:
            start_time = time.time()
            print(pool.map(read_article_jsonl, range(1)))
            print(str(i), "--- %s seconds ---" % (time.time() - start_time))