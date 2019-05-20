# -*- coding: utf-8 -*-
"""
Created on Sun May 19 17:05:09 2019

@author: Anirban
"""

from multiprocessing import Pool
import os, time
from nltk.tokenize import word_tokenize

# Path to json files
# For the limited local memory, I copied article 13 and 14 to the following directory
directory = 'C:/Users/Anirban/Desktop/Masters/MSDSC/DSC550/Excercise/data/wikipedia/featured-articles-excercise10.2/'

# Read all json files from the directory
json_files = [entry.path
              for entry in os.scandir(directory) if entry.name.endswith('.jsonl')]


def tokenize_json_articles(x):
    """
    Args:
        default
    Output:
        data read from the json file(s)
    """
    
    for i in json_files:
        with open(i,'r') as fi:
            tokens = word_tokenize(fi.read())

if __name__ == '__main__':
    
    # define number of processors
    n_processes = [1,2,4,8,16]
    
    # measure execution time for each processor scenarios
    for i in n_processes:
        with Pool(i) as pool:
            start_time = time.time()
            print(pool.map(tokenize_json_articles, range(5)))
            print(str(i), "--- %s seconds ---" % (time.time() - start_time))