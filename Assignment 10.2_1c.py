# -*- coding: utf-8 -*-
"""
Created on Sun May 19 21:34:37 2019

@author: Anirban
"""

from multiprocessing import Pool
from functools import reduce
import os, time, json, string, re
import pandas as pd
from nltk.corpus import stopwords
from collections import Counter

# Create stop words
stop_words = stopwords.words('english')

# Path to json files
# For the limited local memory, I copied article 13 and 14 to the following directory
directory = 'C:/Users/Anirban/Desktop/Masters/MSDSC/DSC550/Excercise/data/wikipedia/featured-articles-excercise10.2/'

# Read all json files from the directory
json_files = [entry.path
              for entry in os.scandir(directory) if entry.name.endswith('.jsonl')]

# Read the json files as data frame
def read_files(json_files):
    
    records = []
    outdf = pd.DataFrame()
    
    for i in json_files:
        with open(i,'r') as fi:
            for line in fi:
               records.append(json.loads(line))
            tempdf = pd.DataFrame(records)
            
        outdf = outdf.append(tempdf)

    return outdf

# Make everything lower case, remove punctuation and newline
def clean_text(df):
    punc = string.punctuation.replace('<', '').replace('>', '')
    pat = re.compile(f'[{punc}]')
    
    # Change text to lower case
    df = df.apply(lambda x: x.astype(str).str.lower())
    
    # Remove punctuation
    df = df.replace(pat, '')
    
    # Replace newline
    df = df.replace(r'\\n',' ', regex=True)
    
    df = df.replace(r'\\',' ', regex=True)
    
    return df

# Create set of words from each data frame text column
def create_wordset(df, col):
    results = set()
    df[col].str.split().apply(results.update)
    return results

def mapper(x):
    text = clean_text(pd.DataFrame(read_files(json_files)['section_texts']))
    text['texts'] = text['section_texts'].apply(lambda x:' '.join([word for word in x.split() if word not in (stop_words)]))
    text['texts'].str.cat(sep=' ')

    # Extract words from text and count
    words = {}
    col = 'texts'

    words = create_wordset(text, col)

    Counter(words).most_common()

    # Count number of times each word comes up in list of words
    d = {};

    for key in words: 
        d[key] = d.get(key, 0) + 1

    sorted(d.items(), key = lambda x: x[1], reverse = True)
    
if __name__ == '__main__':
    
    # define number of processors
    n_processes = [1,2,4,8,16]
    
    # measure execution time for each processor scenarios
    for i in n_processes:
        with Pool(i) as pool:
            start_time = time.time()
            print(pool.map(mapper, range(5)))
            print(str(i), "--- %s seconds ---" % (time.time() - start_time))

