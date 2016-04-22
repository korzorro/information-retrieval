
def calc_edit_distance(s1, s2):
    l1 = len(s1)
    l2 = len(s2)
    dist_matrix = [[0 for x in range(l2+1)] for x in range(l1+1)]
    for i in range(1, l1+1):
        dist_matrix[i][0] = i
    for j in range(1, l2+1):
        dist_matrix[0][j] = j

    for i in range(1, l1+1):
        for j in range(1, l2+1):
            dist_matrix[i][j] = min(dist_matrix[i-1][j-1] + \
                                    (0 if s1[i-1] == s2[j-1] else 1),
                                    dist_matrix[i-1][j] + 1,
                                    dist_matrix[i][j-1] + 1)
    return dist_matrix[l1][l2]


def get_vocabulary(filename):
    with open(filename) as infile:
        return {line.strip() for line in infile}



def find_nearest_word(word, vocabulary):
    def ed(s1):
        return (s1, calc_edit_distance(s1, word))
    return min(map(ed, vocabulary), key=lambda s: s[1])


def make_kword_index(vocabulary, k):
    kword_index = dict()
    for word in vocabulary:
        for kgram in make_kgrams(word, k):
            if kword_index.get(kgram):
                kword_index[kgram] += [word]
            else:
                kword_index[kgram] = [word]
    return kword_index


def make_kgrams(word, k):
    return [word[i:i+k] for i in range(len(word)-k+1)]


def kgram_jaccard(s1, s2):
    n = float(len(set(s1).intersection(set(s2))))
    d = len(set(s1).union(set(s2)))
    return n/d


def lookup_kword_index(word, kword_index, k):
    s = set()
    for gram in make_kgrams(word, k):
        if kword_index.get(gram):
            s |= set(kword_index[gram])
    return s


if __name__ == '__main__':
    K = 3
    all_words = get_vocabulary('vocabulary.txt')
    kword_index = make_kword_index(all_words, K)
    word = raw_input('Enter a word (Enter to exit): ')
    jaccard_threshold = .4
    
    while len(word) > 0:
        vocabulary = filter(lambda x: kgram_jaccard(word, x) > jaccard_threshold, 
                            lookup_kword_index(word, kword_index, K))
        # vocabulary = all_words
        nearest_word, edit_distance = find_nearest_word(word, vocabulary)
        if edit_distance == 0:
            print('*%s* was found in the dictionary.' % nearest_word)
        elif edit_distance > 3:
            print('Could not find *%s* in the dictionary' % word)
            
        else:
            print('Did you mean *%s*?' % nearest_word)
            print(kgram_jaccard(make_kgrams(nearest_word, K), make_kgrams(word, K)))
        word = raw_input('Enter a word (Enter to exit): ')
