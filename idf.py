from math import log
from glob import glob


def idf(term, docs):
    N = float(len(docs))
    n = count_docs_containing_term(term, docs)
    if n == 0:
        n = .0000000001
    if N == 0.0:
        N = .000000001
    return log(N/n)


def count_docs_containing_term(term, docs):
    count = 0
    for doc in docs:
        if doc_contains_term(term, doc):
            count += 1
    return count


def doc_contains_term(term, doc):
    for line in doc:
        for word in line.split(' '):
            if word == term:
                return True


def search():
    docs = map(open, glob('test-docs/*'))
    term = raw_input('Enter a search term: ')
    print(idf(term, docs))


if __name__ == '__main__':
    search()
