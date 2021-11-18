from marshmallow import Schema, fields, post_load


class Word:

    def __init__(self, text, lemma, pos, tag, dep, shape, is_alpha, is_stop, lang, translation, translation_simple,
                 translation_simple_lemma, count):
        self.text = text
        self.lemma = lemma
        self.pos = pos
        self.tag = tag
        self.dep = dep
        self.shape = shape
        self.is_alpha = is_alpha
        self.is_stop = is_stop
        self.lang = lang
        self.translation = translation
        self.translation_simple = translation_simple
        self.translation_simple_lemma = translation_simple_lemma
        self.count = count

    def increase_count(self):
        self.count += 1

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
    tag = fields.Str()
    dep = fields.Str()
    shape = fields.Str()
    is_alpha = fields.Str()
    is_stop = fields.Str()
    lang = fields.Str()
    translation = fields.Str()
    translation_simple = fields.Str()
    translation_simple_lemma = fields.Str()
    count = fields.Integer()

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
