from tkinter import *
from tkinter import Menu
from tkinter import messagebox
from tkinter import Text

import game_logic

class WordGuessUI:
    def __init__(self, master):
        self.master = master
        self.master.title('Word Guess')
        self.master.geometry('750x700')
        self.master.configure(background='#171826')
        self.master.resizable(width=False, height=False)

        self.word_to_guess = game_logic.init_game()
        self.guesses_left = 6
        self.word_bank = self.load_word_bank()

        self.text_widget = Text(
            self.master,
            height=1,
            width=15,
            bg='#2B2D47',
            fg='#FFFFF8',
            borderwidth=0,
            font=('Calibri Bold', 50),
        )
        self.text_widget.pack()

        self.text_widget.insert(END, '   W')
        self.text_widget.insert(END, 'O', 'color_orange')
        self.text_widget.insert(END, 'RD  ')
        self.text_widget.insert(END, 'G', 'color_green')
        self.text_widget.insert(END, 'UESS')

        self.text_widget.tag_configure('color_green', foreground='#11FF38')
        self.text_widget.tag_configure('color_orange', foreground='#FF9811')
        self.text_widget.configure(state=DISABLED)

        self.text_widget.place(
            relx=0.5,
            rely=0.1,
            anchor='center'
        )

        self.text_info1 = Text(
            self.master,
            fg='#FFFFF8',
            wrap=WORD,
            background='#171826',
            font=('Calibri bold', 15),
            height=10,
            width=19,
            highlightthickness=0,
            bd=0
        )
        self.text_info1.insert(
            END,
            'Green\n',
            'color_green'
        )
        self.text_info1.insert(
            END,
            'The letter is present in the word and is in the right position'
        )
        self.text_info1.tag_configure('color_green', foreground='#11FF38')
        self.text_info1.configure(state=DISABLED)
        self.text_info1.tag_configure('justify', justify='right')
        self.text_info1.tag_add('justify', '1.0', END)

        self.text_info1.place(
            relx=0.02,
            rely=0.3,
        )

        self.text_info2 = Text(
            self.master,
            fg='#FFFFF8',
            wrap=WORD,
            background='#171826',
            font=('Calibri bold', 15),
            height=10,
            width=19,
            highlightthickness=0,
            bd=0
        )
        self.text_info2.insert(
            END,
            'Orange\n',
            'color_orange'
        )
        self.text_info2.insert(
            END,
            'The letter is present in the word, but in a different position'
        )
        self.text_info2.tag_configure('color_orange', foreground='#FF9811')
        self.text_info2.configure(state=DISABLED)

        self.text_info2.place(
            relx=0.73,
            rely=0.3,
        )

        self.user_input = Entry(
            self.master,
            width=10,
            font=('Arial Bold', 20),
            justify='center',
            background='#2B2D47',
            fg='#FFFFF8',
        )
        self.user_input.place(
            relx=0.5,
            rely=0.9,
            anchor='center',
        )

        self.dig_field = Text(
            self.master,
            font=('Arial Bold', 46),
            bg='#2B2D47',
            fg='#FFFFF8',
            highlightthickness=0,
            bd=0,
            wrap=WORD,
            state='disabled',
        )

        self.dig_field.tag_configure('center', justify='center')
        
        self.dig_field.place(
            width=300,
            height=420,
            relx=0.5,
            rely=0.5,
            anchor='center',
        )

        self.dig_field.tag_configure('green_tag', foreground='#11FF38')
        self.dig_field.tag_configure('orange_tag', foreground='#FF9811')
        self.dig_field.tag_configure('default_tag', foreground='#FFFFF8')

        self.menu = Menu(self.master, bg='#2B2D47', fg='#FFFFFF')
        self.new_item = Menu(self.menu, tearoff=0, bg='#2B2D47', fg='#11FF38')
        self.new_item.add_command(label='New game', command=self.new_game)
        self.menu.add_cascade(label='Menu', menu=self.new_item)
        self.master.config(menu=self.menu)
        self.guesses = []
        self.user_input.bind('<Return>', self.check_guess)

    def load_word_bank(self, word_file='words.txt'):
        word_bank = []
        with open(word_file) as f:
            for line in f:
                if len(line.strip()) == 5:
                    word_bank.append(line.strip().lower())
        return word_bank

    def check_guess(self, event = None):
        guess = self.user_input.get().lower()

        if guess not in self.word_bank:
            messagebox.showerror('Error', 'This word is not in the dictionary.')
            return

        correct, misplaced, incorrect = game_logic.check_guess(guess, self.word_to_guess)

        if len(correct) == 5:
            messagebox.showinfo('Go!', 'Correct word!')
            self.user_input.config(state=DISABLED)
        else:
            self.guesses_left -= 1
            if self.guesses_left == 0:
                messagebox.showinfo('oG!', f'You lose! The correct word: {self.word_to_guess}')
                self.user_input.config(state=DISABLED)

        self.guesses.append((guess, correct, misplaced, incorrect))
        self.update_dig_field()
        self.user_input.delete(0, END)

    def update_dig_field(self):
        self.dig_field.config(state=NORMAL)
        self.dig_field.delete('1.0', END)

        for guess, correct, misplaced, incorrect in self.guesses:
            for i, letter in enumerate(guess):
                if letter in correct:
                    tag = 'green_tag'
                elif letter in misplaced:
                    tag = 'orange_tag'
                else:
                    tag = 'default_tag'
                self.dig_field.insert(END, letter, tag)
            self.dig_field.insert(END, '\n')

        self.dig_field.config(state=DISABLED)

    def new_game(self):
        self.word_to_guess = game_logic.init_game()
        self.guesses_left = 6
        self.guesses = []
        self.user_input.config(state=NORMAL)
        self.update_dig_field()

root = Tk()
ui = WordGuessUI(root)
root.mainloop()