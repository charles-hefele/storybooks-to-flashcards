from word import VocabularySchema
import tkinter as tk
from tkinter import ttk
from random import randint

# BOOK = 'Meine Sachen'
BOOK = 'kasperle_auf_reisen_ch1'
VOCAB_INPUT = f'vocab/{BOOK}.json'
SHUFFLE = False

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 450
LEFT_ALIGN = WINDOW_WIDTH / 2 - 100

class App(tk.Tk):

    def __init__(self):
        super().__init__()

        self.style = ttk.Style(self)
        self.style.theme_use('aqua')

        # init vocab
        with open(VOCAB_INPUT, 'r') as file:
            contents = file.read()
            self.vocab = VocabularySchema().loads(contents)

        # init first card
        if SHUFFLE:
            self.card = self.get_new_shuffled_card()
        else:
            self.card = 0

        # init card side
        self.side = 0

        # configure the root window
        self.title(f'Storybooks-to-Flashcards')
        self.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}')

        # title label
        self.lbl_title = ttk.Label(self, text=f'Vocabulary for', font=('Helvetica', 20))
        self.lbl_title.pack(pady=20)

        # book label
        self.lbl_book = ttk.Label(self, text=BOOK, font=('Helvetica', 30, 'italic'))
        self.lbl_book.pack(pady=0)

        # word label
        self.lbl_word = ttk.Label(self, text=self.vocab.words[self.card].text, font=('Helvetica', 60))
        self.lbl_word.pack(pady=40)

        # lemma label
        self.lbl_lemma = ttk.Label(self, text=f'Lemma: {self.vocab.words[self.card].lemma}', font=('Helvetica', 18))
        self.lbl_lemma.pack(pady=0, anchor='w', padx=(LEFT_ALIGN, 0))

        # pos label
        self.lbl_pos = ttk.Label(self, text=f'Part of speech: {self.vocab.words[self.card].pos}', font=('Helvetica', 18))
        self.lbl_pos.pack(pady=0, anchor='w', padx=(LEFT_ALIGN, 0))

        # lang label
        lang = 'English' if self.side else 'German'
        self.lbl_lang = ttk.Label(self, text=f'Language: {lang}', font=('Helvetica', 18))
        self.lbl_lang.pack(pady=0, anchor='w', padx=(LEFT_ALIGN, 0))

        # instruction label
        self.lbl_instruction = ttk.Label(self, text='<- Previous    Space: Flip card    Next ->', font=('Helvetica', 18))
        self.lbl_instruction.pack(pady=30)

        # keyboard bindings
        self.bind('<space>', self.flip_card)
        self.bind('<Right>', self.next_card)
        self.bind('<Left>', self.previous_card)

    def flip_card(self, event):
        self.side ^= 1
        new_text = self.vocab.words[self.card].translation if self.side else self.vocab.words[self.card].text
        self.lbl_word.config(text=new_text)
        self.lbl_lang.config(text='Language: English' if self.side else 'Language: German')

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
        self.side = 0   # restore to German
        self.lbl_word.config(text=self.vocab.words[self.card].text)
        self.lbl_lang.config(text='Language: English' if self.side else 'Language: German')
        self.lbl_lemma.config(text=f'Lemma: {self.vocab.words[self.card].lemma}')
        self.lbl_pos.config(text=f'Part of speech: {self.vocab.words[self.card].pos}')


if __name__ == "__main__":
    app = App()
    app.mainloop()
