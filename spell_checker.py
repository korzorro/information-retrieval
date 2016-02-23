
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


def make_nearest_word_finder(vocabulary):
    def find_nearest_word(word):
        def ed(s1):
            return (s1, calc_edit_distance(s1, word))
        return min(map(ed, vocabulary), key=lambda s: s[1])
    return find_nearest_word


if __name__ == '__main__':
    find_nearest_word = make_nearest_word_finder(get_vocabulary('vocabulary.txt'))
    word = raw_input('Enter a word (Enter to exit): ')
    while len(word) > 0:
        nearest_word, edit_distance = find_nearest_word(word)
        if edit_distance == 0:
            print('*%s* was found in the dictionary.' % nearest_word)
        elif edit_distance > 3:
            print('Could not find *%s* in the dictionary' % word)
        else:
            print('Did you mean *%s*?' % nearest_word)
        word = raw_input('Enter a word (Enter to exit): ')
