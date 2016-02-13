import re
from glob import glob
from copy import deepcopy

DOC_DIR = 'test_docs'
NOT_WORD_RE = '[^\w]'
ops = {'and': set.intersection,
       'or': set.union,
       'not': set.difference}


def run():
    docs = collect_documents_as_strings()
    postings_list = make_postings_list(docs)
    query = get_query('Enter a search query (Enter to quit): ')
    while len(query[0]) > 0:
        retrieved = binary_retrieve(postings_list, deepcopy(query), len(docs))
        test_results(retrieved, query)
        print('Found documents: %d' % len(retrieved))
        query = get_query('Enter a search query (Enter to quit): ')
        


def collect_documents_as_strings():
    docs = []
    for filename in glob(DOC_DIR + '/*'):
        with open(filename) as readfile:
            docs.append((filename, tokenize(readfile.read())))
    return docs


def tokenize(doc):
    doc = doc.replace('\n', '').lower()
    return re.sub(NOT_WORD_RE, ' ', doc).split()


def make_postings_list(docs):
    postings_list= dict()
    for doc_id, doc in docs:
        for token in doc:
            if token in postings_list:
                postings_list[token].add(doc_id)
            else:
                postings_list[token] = {doc_id}
    return postings_list


def get_query(prompt):
    return parse_query(raw_input(prompt))

    
def parse_query(query):
    return infix_postfix(query.lower().split(' '))

    
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
    all_docs = range(num_docs)
    pages_found = set()
    def _binary_retrieve(query):
        op = query.pop()
        if op == 'not':
            return ops[op](all_docs,  _binary_retrieve(query))
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


# For now only tests 'AND' cases
def test_results(retrieved, query):
    for filename in retrieved:
        with open(filename) as foundfile:
            text = foundfile.read().lower()
            for term in query:
                if term not in ops:
                    if not (term in text):
                        print('Test failed')
                        print('Filename: %s' % filename)
                        print('Term: %s' % term)
                        exit()

    
if __name__ == '__main__':
    run()
