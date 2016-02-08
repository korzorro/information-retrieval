import re
from glob import glob


NOT_WORD_RE = '[^\w]'


def index(docs):
    docs = zip(map(wordify, docs), range(len(docs)))
    dictionary = dict()
    for doc, doc_id in docs:
        for word in doc:
            if word in dictionary:
                dictionary[word].add(doc_id)
            else:
                dictionary[word] = {doc_id}
    return dictionary


def wordify(doc):
    doc = doc.read().replace('\n', '').lower()
    return re.sub(NOT_WORD_RE, ' ', doc).split()


def lookup(query, dictionary):
    pages_found = None
    for term in query:
        if dictionary.get(term):
            if pages_found:
                pages_found &= dictionary.get(term)
            else:
                pages_found = dictionary.get(term)
    return pages_found


def test():
    docs = map(open, glob('test_docs/*'))
    dictionary = index(docs)
    query = raw_input('Enter a search term: ').lower().split(' ')
    print(lookup(query, dictionary))

    
if __name__ == '__main__':
    test()
