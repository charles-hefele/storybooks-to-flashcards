from tkinter import *
from tkinter import ttk
from word import VocabularySchema

# BOOK = 'Meine Sachen'
# BOOK = 'Mein Zoo Gucklochbuch'
# BOOK = 'Der Kleine König - Teddy ist weg'
# BOOK = 'Kasperle auf Reisen - Chapter 1'
BOOK = 'Kasperle auf Reisen'

VOCAB_INPUT = f'vocab/{BOOK}.json'
ROWS = 40

# SORT = 'chrono'
SORT = 'count'
# SORT = 'alpha'
# SORT = 'pos'
# SORT = 'lemma'

# read the data
with open(VOCAB_INPUT, 'r') as file:
    contents = file.read()
    vocab = VocabularySchema().loads(contents)

ws = Tk()
ws.title("Storybooks-to-Flashcards")

frame = Frame(ws)
frame.pack()

tv = ttk.Treeview(frame, columns=(0, 1, 2, 3, 4, 5, 6, 7), show='headings', height=ROWS)
tv.pack(side=LEFT)

NARROW_COLUMN_WIDTH = 40
STANDARD_COLUMN_WIDTH = 150
WIDE_COLUMN_WIDTH = 290

tv.heading(0, text='#')
tv.column(0, width=NARROW_COLUMN_WIDTH)

tv.heading(1, text='Count')
tv.column(1, width=NARROW_COLUMN_WIDTH)

tv.heading(2, text='German')
tv.column(2, width=STANDARD_COLUMN_WIDTH)

tv.heading(3, text='English')
tv.column(3, width=STANDARD_COLUMN_WIDTH)

tv.heading(4, text='Lemma')
tv.column(4, width=STANDARD_COLUMN_WIDTH)

tv.heading(5, text='English Lemma')
tv.column(5, width=STANDARD_COLUMN_WIDTH)

tv.heading(6, text='Part of Speech')
tv.column(6, width=WIDE_COLUMN_WIDTH)

tv.heading(7, text='Sentences')
tv.column(7, width=WIDE_COLUMN_WIDTH)

sb = Scrollbar(frame, orient=VERTICAL)
sb.pack(side=RIGHT, fill=Y)

tv.config(yscrollcommand=sb.set)

# sort the list
if SORT == 'count':
    vocab.words.sort(key=lambda x: x.count, reverse=True)
elif SORT == 'alpha':
    vocab.words.sort(key=lambda x: x.text)
elif SORT == 'pos':
    vocab.words.sort(key=lambda x: x.pos)
elif SORT == 'lemma':
    vocab.words.sort(key=lambda x: x.lemma)

# populate the columns
num = 1
for w in vocab.words:
    tv.insert(parent='', index=END, values=(num, w.count, w.text, w.text_trans, w.lemma, w.lemma_trans, w.pos,
                                            str(w.sentences)))
    num += 1

ws.mainloop()
