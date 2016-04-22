#!/usr/bin/python3

import re
from glob import glob
from copy import deepcopy
from math import log
from arguments import get_arguments

DOC_DIR = 'test_docs'
NOT_WORD_RE = '[^\w]'
ops = {'and': set.intersection,
       'or': set.union,
       'not': set.difference}
args = get_arguments()


def idf(term, docs):
    N = len(docs)
    df = count_docs_containing_term(term, [doc[1] for doc in docs])
    if df == 0:
        return 0
    else:
        return log(N/df)


def tf(term, doc):
    count = 0
    for word in doc:
        if word == term:
            count += 1
    return count


def count_docs_containing_term(term, docs):
    count = 0
    for doc in docs:
        if doc_contains_term(term, doc):
            count += 1
    return count


def doc_contains_term(term, doc):
    for word in doc:
        if word == term:
            return True

        
def load_docs(directory, dictionary):
    docs = []
    i = 0
    for filename in glob(directory + '/*'):
        i += 1
        if i > 2:
            break
        with open(filename) as readfile:
            docs.append((filename, tokenize(readfile.read(), dictionary)))
    return docs


def tokenize(doc, dictionary):
    doc = doc.replace('\n', '').lower()
    doc = re.sub(NOT_WORD_RE, ' ', doc).split()
    doc = list(filter(lambda w: w in dictionary, doc))
    return doc


def make_postings_list(docs):
    postings_list= dict()
    idf_list = dict()
    for doc_id, doc in docs:
        count = 0
        for token in set(doc):
            if token not in idf_list:
                idf_list[token] = idf(token, docs)
            if postings_list.get(token):
                postings_list[token][doc_id] = tf(token, doc)
            else:
                count += 1
                postings_list[token] = {doc_id: tf(token, doc) * idf_list[token],
                                        'idf': idf_list[token]}
        print(count)
    return postings_list


def get_query(prompt):
    return parse_query(input(prompt))

    
def parse_query(query):
    return query.lower().split(' ')

    
def infix_postfix(tokens):
    output = []
    stack = []
    for item in tokens:
        if item in ops:
            while stack:
                output.append(stack.pop())
            stack.append(item)
        else:
            output.append(item)
    while stack:
        output.append(stack.pop())
    return output


def binary_retrieve(postings_list, query, num_docs):
    all_docs = set()
    for term in postings_list:
        all_docs |= postings_list[term]
    pages_found = set()
    def _binary_retrieve(query):
        op = query.pop()
        if op == 'not':
            return all_docs -  _binary_retrieve(query)
        elif op == 'and' or op == 'or':
            op1 = _binary_retrieve(query)
            op2 = _binary_retrieve(query)
            return ops[op](op1, op2)
        else:
            found = postings_list.get(op)
            if found:
                return found
            else:
                return set()
            
    return _binary_retrieve(query)



def ranked_retrieve(postings_list, query, max_retrieve=10):
    scores = dict()
    for term in query:
        postings_of_term = postings_list.get(term)
        if postings_of_term:
            term_weight = postings_of_term['idf']
            for doc_id, weight in postings_list[term].items():
                if scores.get(doc_id):
                    scores[doc_id] += weight * term_weight
                else:
                    scores[doc_id] = weight * term_weight
    return scores
    

def save_postings_list(filename, postings_list):
    with open(filename, 'w') as postings_list_file:
        for token, val in postings_list.items():
            postings_list_file.write('%s, ' % token)
            postings_list_file.write('%s, ' % val['idf'])
            for doc_id, tf in val.items():
                if doc_id != 'idf':
                    postings_list_file.write('%s:%s ' % (doc_id, tf))
            postings_list_file.write('\n')


if __name__ == '__main__':
    print('Reading docs...')
    dictionary = set()
    with open('vocabulary.txt') as vocab:
        for word in vocab:
            dictionary.add(word.strip())
    docs = load_docs(DOC_DIR, dictionary)
    print('Done.')
    print('Generating postings list...')
    postings_list = make_postings_list(docs)
    print('Done.')
    print('Saving postings list...')
    filename = 'postings.post'
    save_postings_list(filename, postings_list)
    query = get_query('Enter a search query (Enter to quit): ')
    if args.b:
        query = infix_postfix(query)
        retrieved = binary_retrieve(postings_list, deepcopy(query), len(docs))
        print('Found documents: %d' % len(retrieved))
        query = get_query('Enter a search query (Enter to quit): ')
    else:
        retrieved = ranked_retrieve(postings_list, query, max_retrieve=10)
        for document_id, score in retrieved.items():
            print('%s. %s' % (document_id, score))
    
