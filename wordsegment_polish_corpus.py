import polars as pl
from spacy.lang.pl import Polish
from collections import Counter
from multiprocessing import Pool, cpu_count
import json
from tqdm import tqdm
from unidecode import unidecode
from typing import Callable

CHUNK_SIZE = 2000
CORPUS_PATH = 'wiki_2023.txt'
MAX_LENGTH_CHUNK = 990000
REMOVE_DIACRITICS: Callable[[str], str] | None = unidecode
UNIGRAM_FILENAME = 'polish_unigrams_no_diacritics.json'
BIGRAM_FILENAME = 'polish_bigrams_no_diacritics.json'

def split_text_if_needed(text, max_length=990000):
    """
    Splits a long text into a list of smaller texts, each under max_length.
    """
    if len(text) < max_length:
        return [text]

    SEPARATOR = ' \n '
    SEPARATOR_LEN = len(SEPARATOR)
    
    sub_chunks = []
    current_lines_buffer = []
    current_length = 0
    lines = text.split('\n')
    
    for line in lines:
        if len(line) > max_length:
            print(f"Warning: Skipping a single line of length {len(line)}")
            continue

        additional_length = len(line) if not current_lines_buffer else SEPARATOR_LEN + len(line)
        
        if current_length + additional_length > max_length:
            if current_lines_buffer:
                sub_chunks.append(SEPARATOR.join(current_lines_buffer))
            current_lines_buffer = [line]
            current_length = len(line)
        else:
            current_lines_buffer.append(line)
            current_length += additional_length
        
    if current_lines_buffer:
        sub_chunks.append(SEPARATOR.join(current_lines_buffer))
        
    return sub_chunks


def read_in_chunks(file_path, chunk_size=10000):
    """
    FIXED: Actually streams the file without loading everything into memory.
    """
    current_batch = []
    
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                current_batch.append(line)
            
            if len(current_batch) >= chunk_size:
                yield ' \n '.join(current_batch)
                current_batch = []  
        
        
        if current_batch:
            yield ' \n '.join(current_batch)


def process_chunk(text_chunk):
    """
    Processes a single chunk of text: tokenizes and counts unigrams/bigrams.
    """
    nlp = Polish()
    
    sub_chunks_to_process = split_text_if_needed(text_chunk, max_length=MAX_LENGTH_CHUNK)
    
    total_unigrams = Counter()
    total_bigrams = Counter()
    for sub_chunk in sub_chunks_to_process:
        if not sub_chunk.strip():
            continue
        
        
        sub_chunk = sub_chunk if not REMOVE_DIACRITICS else REMOVE_DIACRITICS(sub_chunk)
        tokens_for_chunk = [t.text.lower() for t in nlp.make_doc(sub_chunk) if t.is_alpha]
        
        
        total_unigrams.update(tokens_for_chunk)
        total_bigrams.update(pairs(tokens_for_chunk))
        
        
        del tokens_for_chunk
    
    
    del sub_chunks_to_process
    
    return total_unigrams, total_bigrams


def pairs(tokens):
    """Generator for creating bigrams."""
    for i in range(len(tokens) - 1):
        yield f"{tokens[i]} {tokens[i+1]}"


if __name__ == '__main__':
    file_path = 'wiki_2023.txt'
    
    
    total_unigrams = Counter()
    total_bigrams = Counter()

    num_processes = max(1, cpu_count() - 1)  
    print(f"Starting parallel processing with {num_processes} cores...")

    
    with Pool(processes=num_processes) as pool:
        results_iterator = pool.imap_unordered(
            process_chunk, 
            read_in_chunks(file_path, chunk_size=CHUNK_SIZE),
            chunksize=1  
        )
        
        
        for partial_unigrams, partial_bigrams in tqdm(results_iterator, desc="Processing Chunks"):
            total_unigrams.update(partial_unigrams)
            total_bigrams.update(partial_bigrams)
            
            
            del partial_unigrams
            del partial_bigrams

    print("\nParallel processing complete...")

  
    print(f"Total unique unigrams: {len(total_unigrams)}")
    print(f"Total unique bigrams: {len(total_bigrams)}")
    
    
    print(f"\nSaving unigram counts to {UNIGRAM_FILENAME}...")
    with open(UNIGRAM_FILENAME, 'w', encoding='utf-8') as f:
        json.dump(total_unigrams, f, ensure_ascii=False, indent=2)  
    
    print(f"Saving bigram counts to {BIGRAM_FILENAME}...")
    with open(BIGRAM_FILENAME, 'w', encoding='utf-8') as f:
        json.dump(total_bigrams, f, ensure_ascii=False, indent=2)
    
    print("\nAll tasks completed successfully!")