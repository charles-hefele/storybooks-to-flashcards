from marshmallow import Schema, fields, post_load


class Word:

    def __init__(self, text, lemma, pos, text_trans=None, lemma_trans=None, count=1, sentences=None):
        self.text = text
        self.lemma = lemma
        self.pos = pos
        self.text_trans = text_trans
        self.lemma_trans = lemma_trans
        self.count = count
        if sentences is None:
            self.sentences = []
        else:
            self.sentences = sentences

    def increase_count(self):
        self.count += 1

    def add_new_sentence(self, sentence):
        self.sentences.append(sentence)

    def shorthand(self):
        return str(f'{self.count}, {self.lemma}, {self.lemma_trans}, {self.text}, {self.text_trans}, {self.pos}, '
                   f'{self.sentences}\n')

    def __eq__(self, other):
        if isinstance(other, Word):
            return self.text == other.text and self.pos == other.pos
        return False

    def __repr__(self):
        return str(vars(self))


class WordSchema(Schema):
    text = fields.Str()
    lemma = fields.Str()
    pos = fields.Str()
    text_trans = fields.Str(allow_none=True)
    lemma_trans = fields.Str(allow_none=True)
    count = fields.Integer()
    sentences = fields.List(fields.Str)

    @post_load
    def make_object(self, data, **__):
        return Word(**data)


class Vocabulary:
    def __init__(self, words):
        self.words = words

    def __repr__(self):
        return str(vars(self))


class VocabularySchema(Schema):
    words = fields.Nested(WordSchema, many=True)

    @post_load(pass_many=True)
    def make_object(self, data, **__):
        return Vocabulary(**data)
