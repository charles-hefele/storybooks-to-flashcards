from vec_math import *
import numpy as np


class SpacyVecOps:

    def __init__(self, nlp):
        self.nlp = nlp

    def vec(self, word):
        return self.nlp.vocab[word].vector

    def closest_words(self, tokens, query, n=10):
        return sorted(tokens,
                      key=lambda x: cos(self.vec(query), self.vec(x)),
                      reverse=True)[:n]

    def closest_words_vocab(self, words, query, n=10):
        return sorted(words,
                      key=lambda x: cos(self.vec(query), self.vec(x.text)),
                      reverse=True)[:n]

    def sentence_to_vec(self, s):
        sent = self.nlp(s)
        return mean([w.vector for w in sent])

    def closest_sentences(self, sentences, input_str, n=10):
        input_vec = self.sentence_to_vec(input_str)
        return sorted(sentences,
                      key=lambda x: cos(np.mean([w.vector for w in x], axis=0), input_vec),
                      reverse=True)[:n]
