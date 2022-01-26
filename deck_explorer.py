import spacy
from word import VocabularySchema
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from spacy_vec_ops import SpacyVecOps

BOOKS = [
    'Kasperle auf Reisen',
    'Kasperle auf Reisen - Chapter 1',
    'Gute Nacht, kleiner Löwe!',
    'Meine Sachen',
    'Mein Zoo Gucklochbuch',
    'Der Kleine König - Teddy ist weg'
]

BOOK = BOOKS[0]

VOCAB_INPUT = f'vocab/{BOOK}.json'
SHOW_LEMMAS = False
WINDOW_WIDTH = 1250
WINDOW_HEIGHT = 740
SPACE_FROM_LEFT_MARGIN = 20
SPACE_BETWEEN_WORDS = 5
FONT_HEADER = 20
FONT_GRID = 18
PAD_X = 10
NUM_SEARCH_RESULTS = 25
INITIAL_WORD = 'Tier'
MSG_SHOWING = 'Showing top {} related words for \'{}\':'
MSG_STATS = '{} cards, {} unique words, {} unique lemmas, constructed from {} words'

def destroy_widgets(frame):
    for widget in frame.winfo_children():
        widget.destroy()


class App(tk.Tk):

    def __init__(self):
        super().__init__()

        # init widget containers
        self.terms_text = []
        self.terms_text_trans = []
        self.terms_lemma = []
        self.terms_lemma_trans = []
        self.terms_pos = []
        self.terms_count = []

        # init search term
        self.search_term = tk.StringVar()

        # load the model
        self.nlp = spacy.load('de_core_news_lg')
        self.ops = SpacyVecOps(self.nlp)

        # set style
        self.style = ttk.Style(self)
        self.style.theme_use('aqua')

        # init vocab
        self.vocab = None

        # configure the root window
        self.title(f'Storybooks-to-Flashcards: Deck Explorer')
        self.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}')

        # create the main containers
        frame_top = ttk.Frame(self)
        frame_middle = ttk.Frame(self)
        self.frame_bottom = ttk.Frame(self)

        # configure the search bar row to have fixed width
        frame_top.columnconfigure(0, minsize=300)

        # layout the main containers
        frame_top.grid(row=0, sticky='w')
        frame_middle.grid(row=1, sticky='w')
        self.frame_bottom.grid(row=2, sticky='w')

        # create and position the stats label
        self.lbl_stats = ttk.Label(frame_top, font=('Helvetica', FONT_HEADER))
        self.lbl_stats.grid(row=1, column=1, padx=PAD_X, sticky='w')

        # create and position the 'showing' label
        self.lbl_showing = ttk.Label(frame_middle, font=('Helvetica', FONT_HEADER))
        self.lbl_showing.grid(row=0, column=0, padx=PAD_X, sticky='w')

        # init the book variable
        self.book = tk.StringVar(self)
        self.book.trace_add('write', self.book_changed)
        self.book.set(BOOKS[0])  # default value

        # create the widgets for the top frame
        lbl_title = ttk.Label(frame_top, text=f'Deck Explorer', font=('Helvetica', FONT_HEADER))
        options = tk.OptionMenu(frame_top, self.book, *BOOKS)
        self.entry = ttk.Entry(frame_top, textvariable=self.search_term)
        button = ttk.Button(frame_top, text='Search', command=self.search)

        # layout the widgets for the top frame
        lbl_title.grid(row=0, column=0, padx=PAD_X, sticky='w')
        options.grid(row=1, column=0, padx=PAD_X, sticky='we')
        self.entry.grid(row=2, column=0, padx=PAD_X, sticky='we')
        button.grid(row=2, column=1, padx=PAD_X, sticky='w')

        # bind the enter button
        self.entry.bind('<Return>', lambda event: self.search())
        self.entry.focus_set()

    def search(self):
        term = self.search_term.get()
        if self.ops.search_term_exists(term):
            exploration = self.explore(self.vocab.words, term, NUM_SEARCH_RESULTS)
            self.refresh(term, exploration)
            self.search_term.set('')
        else:
            messagebox.showwarning('Not found', 'No word vector could be found for this word.')
            self.focus_force()
            self.entry.focus_set()

    # when the user clicks one of the words
    def callback(self, obj):
        term = obj['text']  # get the text from the word label that was clicked
        exploration = self.explore(self.vocab.words, term,
                                   NUM_SEARCH_RESULTS)  # the word definitely exists, so no need to check for zero vector here
        self.refresh(term, exploration)

    def explore(self, words, query, count=10):
        return self.ops.closest_words(words, query, count)

    def refresh(self, term, exploration):
        self.lbl_showing.configure(text=MSG_SHOWING.format(NUM_SEARCH_RESULTS, term))
        for i, word in enumerate(exploration):
            self.terms_text[i].config(text=word.text)
            self.terms_text_trans[i].config(text=word.text_trans)
            self.terms_lemma[i].config(text=word.lemma)
            self.terms_lemma_trans[i].config(text=word.lemma_trans)
            self.terms_pos[i].config(text=word.pos)
            self.terms_count[i].config(text=word.count)

    def book_changed(self, *args):
        destroy_widgets(self.frame_bottom)
        self.create_widgets(self.book.get())

    def create_widgets(self, book):
        # initialize the vocabulary object
        with open(f'vocab/{book}.json', 'r') as file:
            contents = file.read()
            self.vocab = VocabularySchema().loads(contents)

        # set the stats string
        stats = MSG_STATS.format(len(self.vocab.words), len(self.vocab.unique_words()), len(self.vocab.unique_lemmas()),
                                 self.vocab.original_word_count)
        self.lbl_stats.config(text=stats)

        # set initial exploration word
        exploration = self.explore(self.vocab.words, INITIAL_WORD, NUM_SEARCH_RESULTS)
        self.lbl_showing.config(text=MSG_SHOWING.format(NUM_SEARCH_RESULTS, INITIAL_WORD))

        # set the widget containers
        self.terms_text = []
        self.terms_text_trans = []
        self.terms_lemma = []
        self.terms_lemma_trans = []
        self.terms_pos = []
        self.terms_count = []

        # create the header widgets for the bottom frame
        lbl_text_header = ttk.Label(self.frame_bottom, text='German', font=('Helvetica bold', FONT_GRID))
        lbl_text_trans_header = ttk.Label(self.frame_bottom, text='English', font=('Helvetica bold', FONT_GRID))
        lbl_lemma_header = ttk.Label(self.frame_bottom, text='Lemma', font=('Helvetica bold', FONT_GRID))
        lbl_lemma_trans_header = ttk.Label(self.frame_bottom, text='Lemma (English)',
                                           font=('Helvetica bold', FONT_GRID))
        lbl_pos_header = ttk.Label(self.frame_bottom, text='Part of Speech', font=('Helvetica bold', FONT_GRID))
        lbl_count_header = ttk.Label(self.frame_bottom, text='Occurrences', font=('Helvetica bold', FONT_GRID))

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
            lbl_num = ttk.Label(self.frame_bottom, text=f'{i + 1}.', font=('Helvetica', FONT_GRID))
            lbl_text = ttk.Label(self.frame_bottom, text=exploration[i].text,
                                 font=('Helvetica', FONT_GRID, 'underline'),
                                 foreground='blue', cursor='hand2')
            lbl_text_trans = ttk.Label(self.frame_bottom, text=exploration[i].text_trans, font=('Helvetica', FONT_GRID))
            lbl_lemma = ttk.Label(self.frame_bottom, text=exploration[i].lemma, font=('Helvetica', FONT_GRID))
            lbl_lemma_trans = ttk.Label(self.frame_bottom, text=exploration[i].lemma_trans,
                                        font=('Helvetica', FONT_GRID))
            lbl_pos = ttk.Label(self.frame_bottom, text=exploration[i].pos, font=('Helvetica', FONT_GRID))
            lbl_count = ttk.Label(self.frame_bottom, text=exploration[i].count, font=('Helvetica', FONT_GRID))

            # layout the search results widgets for the bottom frame
            lbl_num.grid(row=i + 1, column=0, padx=PAD_X, sticky='w')
            lbl_text.grid(row=i + 1, column=1, padx=PAD_X, sticky='w')
            lbl_text_trans.grid(row=i + 1, column=2, padx=PAD_X, sticky='w')
            if SHOW_LEMMAS:
                lbl_lemma.grid(row=i + 1, column=3, padx=PAD_X, sticky='w')
                lbl_lemma_trans.grid(row=i + 1, column=4, padx=PAD_X, sticky='w')
            lbl_pos.grid(row=i + 1, column=5, padx=PAD_X, sticky='w')
            lbl_count.grid(row=i + 1, column=6, padx=PAD_X, sticky='w')

            # add mouse click
            lbl_text.bind("<Button-1>", lambda event, obj=lbl_text: self.callback(obj))

            # add these labels to the label lists
            self.terms_text.append(lbl_text)
            self.terms_text_trans.append(lbl_text_trans)
            self.terms_lemma.append(lbl_lemma)
            self.terms_lemma_trans.append(lbl_lemma_trans)
            self.terms_pos.append(lbl_pos)
            self.terms_count.append(lbl_count)


if __name__ == "__main__":
    app = App()
    app.mainloop()
