import tkinter as tk
from tkinter import ttk
from random import randint
from word import VocabularySchema

BOOK = 'Meine Sachen'
VOCAB_INPUT = f'vocab/{BOOK}.json'
SHUFFLE = False

class App(tk.Tk):

    def __init__(self):
        super().__init__()

        # init hint trackers
        self.hint = ''
        self.hint_count = 0

        # init vocab
        with open(VOCAB_INPUT, 'r') as file:
            contents = file.read()
            self.vocab = VocabularySchema().loads(contents)

        # init first card
        if SHUFFLE:
            self.card = self.get_new_shuffled_card()
        else:
            self.card = 0

        # configure the root window
        self.title('Storybooks-to-Flashcards')
        self.geometry('600x450')

        # german word
        self.german_word = ttk.Label(self, text='', font=('Helvetica', 36))
        self.german_word.pack(pady=50)

        # answer label
        self.answer_label = ttk.Label(self, text='', font=['Helvetica', 20])
        self.answer_label.pack(pady=20)

        # text entry field
        self.my_entry = ttk.Entry(self, font=('Helvetica', 18))
        self.my_entry.pack(pady=20)

        # button frame
        self.button_frame = ttk.Frame(self)
        self.button_frame.pack()

        # answer button
        self.answer_button = ttk.Button(self.button_frame, text='Answer')
        self.answer_button['command'] = self.answer_button_clicked

        # previous button
        self.previous_button = ttk.Button(self.button_frame, text='Previous')
        self.previous_button['command'] = self.previous_button_clicked

        # next button
        self.next_button = ttk.Button(self.button_frame, text='Next')
        self.next_button['command'] = self.next_button_clicked

        # hint button
        self.hint_button = ttk.Button(self.button_frame, text='Hint')
        self.hint_button['command'] = self.hint_button_clicked

        # button frame
        self.button_frame.columnconfigure(0, weight=1)
        self.button_frame.columnconfigure(1, weight=1)

        # button grid layout
        self.answer_button.grid(row=0, column=0, padx=0)
        self.previous_button.grid(row=0, column=1, padx=20)
        self.next_button.grid(row=0, column=2, padx=0)
        self.hint_button.grid(row=0, column=3, padx=20)

        # hint label
        self.hint_label = ttk.Label(self, text='')
        self.hint_label.pack(pady=20)

    def answer_button_clicked(self):
        if self.my_entry.get().lower() == self.vocab.words[self.card].translation.lower():
            self.answer_label.config(text=f'Correct')
        else:
            self.answer_label.config(text=f'Incorrect')

    def previous_button_clicked(self):
        if SHUFFLE:
            self.card = self.get_new_shuffled_card()
        elif self.card > 0:
            self.card -= 1
        self.reset_fields()

    def next_button_clicked(self):
        if SHUFFLE:
            self.card = self.get_new_shuffled_card()
        elif self.card < len(self.vocab.words) - 1:
            self.card += 1
        self.reset_fields()

    def get_new_shuffled_card(self):
        return randint(0, len(self.vocab.words) - 1)

    def reset_fields(self):
        self.answer_label.config(text='')
        self.my_entry.delete(0, tk.END)
        self.hint_label.config(text='')
        self.hint = ''
        self.hint_count = 0
        self.german_word.config(text=self.vocab.words[self.card].text)

    def hint_button_clicked(self):
        if self.hint_count < len(self.vocab.words[self.card].translation):
            self.hint = self.hint + self.vocab.words[self.card].translation[self.hint_count]
            self.hint_label.config(text=self.hint)
            self.hint_count += 1


if __name__ == "__main__":
    app = App()
    app.reset_fields()
    app.mainloop()
