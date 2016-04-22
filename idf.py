#!/usr/bin/python3


from glob import glob


        
    

    
def search(directory, term):
    directory += '/*'
    docs = list(map(open, glob(directory)))
    _idf = idf(term, docs)
    print(_idf)


if __name__ == '__main__':
    directory = 'test_docs'
    term = input('Enter a search term: ')
    search(directory, term)
