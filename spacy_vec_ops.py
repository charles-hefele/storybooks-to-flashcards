import vec_math as vm


class SpacyVecOps:

    def __init__(self, nlp):
        self.nlp = nlp

    def vec(self, word):
        return self.nlp.vocab[word].vector

    def search_term_exists(self, term):
        return self.vec(term).any()

    def closest_words(self, words, query, n=10):
        return sorted(words,
                      key=lambda x: vm.cos(self.vec(query), self.vec(x.text)),
                      reverse=True)[:n]
