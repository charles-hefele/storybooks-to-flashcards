import spacy
from word import VocabularySchema
import tkinter as tk
from tkinter import ttk
from spacy_vec_ops import SpacyVecOps

# BOOK = 'Meine Sachen'
# BOOK = 'Mein Zoo Gucklochbuch'
# BOOK = 'Der Kleine König - Teddy ist weg'
# BOOK = 'Kasperle auf Reisen - Chapter 1'
BOOK = 'Kasperle auf Reisen'

VOCAB_INPUT = f'vocab/{BOOK}.json'
SHOW_LEMMAS = False
WINDOW_WIDTH = 1250
WINDOW_HEIGHT = 740
SPACE_FROM_LEFT_MARGIN = 20
SPACE_BETWEEN_WORDS = 5
FONT_HEADER = 20
FONT_GRID = 18
PAD_X = 10
SEARCH_RESULTS = 25


class App(tk.Tk):

    def __init__(self):
        super().__init__()

        # load the model
        self.nlp = spacy.load('de_core_news_lg')
        self.ops = SpacyVecOps(self.nlp)

        # set style
        self.style = ttk.Style(self)
        self.style.theme_use('aqua')

        # init vocab
        with open(VOCAB_INPUT, 'r') as file:
            contents = file.read()
            self.vocab = VocabularySchema().loads(contents)

        # configure the root window
        self.title(f'Storybooks-to-Flashcards: Deck Explorer')
        self.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}')

        # create the main containers
        frame_top = ttk.Frame(self)
        frame_bottom = ttk.Frame(self)

        # layout the main containers
        frame_top.grid(row=0, sticky='w')
        frame_bottom.grid(row=1, sticky='w')

        # create the widgets for the top frame
        lbl_title = ttk.Label(frame_top, text=f'Deck Explorer', font=('Helvetica', FONT_HEADER))
        lbl_book = ttk.Label(frame_top, text=f'{BOOK} ({len(self.vocab.words)} cards)', font=('Helvetica', FONT_HEADER, 'italic'))
        self.lbl_showing = ttk.Label(frame_top, text='Showing top related words for \'Tier\':', font=('Helvetica', FONT_HEADER))

        # layout the widgets for the top frame
        lbl_title.grid(row=0, column=0, padx=PAD_X, sticky='w')
        lbl_book.grid(row=1, column=0, padx=PAD_X, sticky='w')
        self.lbl_showing.grid(row=2, column=0, padx=PAD_X, sticky='w')

        # set initial exploration word
        exploration = self.explore(self.vocab.words, 'Tier', SEARCH_RESULTS)

        # set the widget containers
        self.terms_text = []
        self.terms_text_trans = []
        self.terms_lemma = []
        self.terms_lemma_trans = []
        self.terms_pos = []
        self.terms_count = []

        # create the header widgets for the bottom frame
        lbl_text_header = ttk.Label(frame_bottom, text='German', font=('Helvetica bold', FONT_GRID))
        lbl_text_trans_header = ttk.Label(frame_bottom, text='English', font=('Helvetica bold', FONT_GRID))
        lbl_lemma_header = ttk.Label(frame_bottom, text='Lemma', font=('Helvetica bold', FONT_GRID))
        lbl_lemma_trans_header = ttk.Label(frame_bottom, text='Lemma (English)', font=('Helvetica bold', FONT_GRID))
        lbl_pos_header = ttk.Label(frame_bottom, text='Part of Speech', font=('Helvetica bold', FONT_GRID))
        lbl_count_header = ttk.Label(frame_bottom, text='Occurrences', font=('Helvetica bold', FONT_GRID))

        # layout the header widgets for the bottom frame
        lbl_text_header.grid(row=0, column=1, padx=PAD_X, sticky='w')
        lbl_text_trans_header.grid(row=0, column=2, padx=PAD_X, sticky='w')
        if SHOW_LEMMAS:
            lbl_lemma_header.grid(row=0, column=3, padx=PAD_X, sticky='w')
            lbl_lemma_trans_header.grid(row=0, column=4, padx=PAD_X, sticky='w')
        lbl_pos_header.grid(row=0, column=5, padx=PAD_X, sticky='w')
        lbl_count_header.grid(row=0, column=6, padx=PAD_X, sticky='w')

        # create the search results widgets for the bottom frame
        for i, word in enumerate(exploration):
            lbl_num = ttk.Label(frame_bottom, text=f'{i+1}.', font=('Helvetica', FONT_GRID))
            lbl_text = ttk.Label(frame_bottom, text=exploration[i].text, font=('Helvetica', FONT_GRID, 'underline'),
                                 foreground='blue', cursor='hand2')
            lbl_text_trans = ttk.Label(frame_bottom, text=exploration[i].text_trans, font=('Helvetica', FONT_GRID))
            lbl_lemma = ttk.Label(frame_bottom, text=exploration[i].lemma, font=('Helvetica', FONT_GRID))
            lbl_lemma_trans = ttk.Label(frame_bottom, text=exploration[i].lemma_trans, font=('Helvetica', FONT_GRID))
            lbl_pos = ttk.Label(frame_bottom, text=exploration[i].pos, font=('Helvetica', FONT_GRID))
            lbl_count = ttk.Label(frame_bottom, text=exploration[i].count, font=('Helvetica', FONT_GRID))

            # layout the search results widgets for the bottom frame
            lbl_num.grid(row=i+1, column=0, padx=PAD_X, sticky='w')
            lbl_text.grid(row=i+1, column=1, padx=PAD_X, sticky='w')
            lbl_text_trans.grid(row=i+1, column=2, padx=PAD_X, sticky='w')
            if SHOW_LEMMAS:
                lbl_lemma.grid(row=i+1, column=3, padx=PAD_X, sticky='w')
                lbl_lemma_trans.grid(row=i+1, column=4, padx=PAD_X, sticky='w')
            lbl_pos.grid(row=i+1, column=5, padx=PAD_X, sticky='w')
            lbl_count.grid(row=i+1, column=6, padx=PAD_X, sticky='w')

            # add mouse click
            lbl_text.bind("<Button-1>", lambda event, obj=lbl_text: self.callback(obj))

            # add these labels to the label lists
            self.terms_text.append(lbl_text)
            self.terms_text_trans.append(lbl_text_trans)
            self.terms_lemma.append(lbl_lemma)
            self.terms_lemma_trans.append(lbl_lemma_trans)
            self.terms_pos.append(lbl_pos)
            self.terms_count.append(lbl_count)

    def callback(self, obj):
        term = obj['text']
        self.lbl_showing.configure(text=f'Showing top related words for \'{term}\':')
        exploration = self.explore(self.vocab.words, term, SEARCH_RESULTS)
        for i, word in enumerate(exploration):
            self.terms_text[i].config(text=word.text)
            self.terms_text_trans[i].config(text=word.text_trans)
            self.terms_lemma[i].config(text=word.lemma)
            self.terms_lemma_trans[i].config(text=word.lemma_trans)
            self.terms_pos[i].config(text=word.pos)
            self.terms_count[i].config(text=word.count)

    def explore(self, words, query, count=10):
        return self.ops.closest_words_vocab(words, query, count)


if __name__ == "__main__":
    app = App()
    app.mainloop()
