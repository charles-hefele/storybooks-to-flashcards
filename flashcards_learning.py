from word import VocabularySchema
import tkinter as tk
from tkinter import ttk
from random import randint

# BOOK = 'Meine Sachen'
# BOOK = 'Mein Zoo Gucklochbuch'
# BOOK = 'Der Kleine König - Teddy ist weg'
# BOOK = 'Kasperle auf Reisen - Chapter 1'
BOOK = 'Kasperle auf Reisen'

VOCAB_INPUT = f'vocab/{BOOK}.json'
SHUFFLE = False
SORT = 'count'

WINDOW_WIDTH = 1250
WINDOW_HEIGHT = 740


class App(tk.Tk):

    def __init__(self):
        super().__init__()

        self.style = ttk.Style(self)
        self.style.theme_use('aqua')

        # init vocab
        with open(VOCAB_INPUT, 'r') as file:
            contents = file.read()
            self.vocab = VocabularySchema().loads(contents)

        # sort the list
        if SORT == 'count':
            self.vocab.words.sort(key=lambda x: x.count, reverse=True)
        elif SORT == 'alpha':
            self.vocab.words.sort(key=lambda x: x.text)
        elif SORT == 'pos':
            self.vocab.words.sort(key=lambda x: x.pos)
        elif SORT == 'lemma':
            self.vocab.words.sort(key=lambda x: x.lemma)

        # init first card
        if SHUFFLE:
            self.card = self.get_new_shuffled_card()
        else:
            self.card = 0

        # configure the root window
        self.title(f'Storybooks-to-Flashcards')
        self.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}')

        pad_x = 20

        # title label
        self.lbl_title = ttk.Label(self, text=f'Vocabulary for', font=('Helvetica', 20))
        self.lbl_title.pack(pady=0, padx=pad_x, anchor='w')

        # book label
        self.lbl_book = ttk.Label(self, text=BOOK, font=('Helvetica', 20, 'italic'))
        self.lbl_book.pack(pady=0, padx=pad_x, anchor='w')

        # German label
        self.lbl_german = ttk.Label(self, text='German', font=('Helvetica', 20))
        self.lbl_german.pack(pady=10, padx=pad_x, anchor='w')

        # text label
        self.lbl_text = ttk.Label(self, text=self.vocab.words[self.card].text, font=('Helvetica', 40))
        self.lbl_text.pack(pady=10, padx=pad_x, anchor='w')

        # English label
        self.lbl_english = ttk.Label(self, text='English', font=('Helvetica', 20))
        self.lbl_english.pack(pady=10, padx=pad_x, anchor='w')

        # text_trans label
        self.lbl_text_trans = ttk.Label(self, text=self.get_text_trans(), font=('Helvetica', 40))
        self.lbl_text_trans.pack(pady=10, padx=pad_x, anchor='w')

        # count label
        self.lbl_count = ttk.Label(self, text=f'Count: {self.vocab.words[self.card].count}', font=('Helvetica', 18))
        self.lbl_count.pack(pady=(30, 0), padx=pad_x, anchor='w')

        # lemma label
        self.lbl_lemma = ttk.Label(self, text=f'Lemma: {self.vocab.words[self.card].lemma}', font=('Helvetica', 18))
        self.lbl_lemma.pack(pady=0, padx=pad_x, anchor='w')

        # lemma_trans label
        self.lbl_lemma_trans = ttk.Label(self, text=f'Lemma translation: {self.get_lemma_trans()}', font=('Helvetica', 18))
        self.lbl_lemma_trans.pack(pady=0, padx=pad_x, anchor='w')

        # pos label
        self.lbl_pos = ttk.Label(self, text=f'Part of speech: {self.vocab.words[self.card].pos}', font=('Helvetica', 18))
        self.lbl_pos.pack(pady=0, padx=pad_x, anchor='w')

        # sentences label
        self.sentences_label = ttk.Label(self, text='Sentences:', font=('Helvetica', 18))
        self.sentences_label.pack(pady=0, padx=pad_x, anchor='w')

        # sentences
        self.lbl_sentences = ttk.Label(self, text=self.build_sentences_string(), font=('Helvetica', 18))
        self.lbl_sentences.pack(pady=0, padx=pad_x, anchor='w')

        # instruction label
        self.lbl_instruction = ttk.Label(self, text='<- Previous\tNext ->', font=('Helvetica', 18))
        self.lbl_instruction.pack(pady=30)

        # keyboard bindings
        self.bind('<Right>', self.next_card)
        self.bind('<Left>', self.previous_card)

    def get_text_trans(self):
        text_trans = self.vocab.words[self.card].text_trans
        return '[no translation]' if text_trans is None else text_trans

    def get_lemma_trans(self):
        lemma_trans = self.vocab.words[self.card].lemma_trans
        return '[no translation]' if lemma_trans is None else lemma_trans

    def build_sentences_string(self):
        return '\n'.join(self.vocab.words[self.card].sentences)

    def previous_card(self, event):
        if SHUFFLE:
            self.card = self.get_new_shuffled_card()
        elif self.card > 0:
            self.card -= 1
        self.reset_fields()

    def next_card(self, event):
        if SHUFFLE:
            self.card = self.get_new_shuffled_card()
        elif self.card < len(self.vocab.words) - 1:
            self.card += 1
        self.reset_fields()

    def get_new_shuffled_card(self):
        return randint(0, len(self.vocab.words) - 1)

    def reset_fields(self):
        self.lbl_text.config(text=self.vocab.words[self.card].text)
        self.lbl_text_trans.config(text=self.get_text_trans())
        self.lbl_count.config(text=f'Count: {self.vocab.words[self.card].count}')
        self.lbl_lemma.config(text=f'Lemma: {self.vocab.words[self.card].lemma}')
        self.lbl_lemma_trans.config(text=f'Lemma translation: {self.get_lemma_trans()}')
        self.lbl_pos.config(text=f'Part of speech: {self.vocab.words[self.card].pos}')
        self.lbl_sentences.config(text=self.build_sentences_string())


if __name__ == "__main__":
    app = App()
    app.mainloop()
