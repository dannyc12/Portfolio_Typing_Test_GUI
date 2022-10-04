import random
from tkinter import *
import time

# ------ Constants ------- #
LIGHT_BLUE = '#B9FFF8'
SEA_FOAM = '#6FEDD6'
CORAL_ORANGE = '#FF9551'
SUNSET_RED = '#FF4A4A'


class MortalType:
    def __init__(self):
        self.root = Tk()
        self.root.title('Test Your Type')
        self.root.geometry('+%d+%d' % (200, 10))
        self.root.config(padx=25, pady=25, bg=LIGHT_BLUE)
        self.running = False
        self.start_time = None
        self.end_time = None
        self.total_time = None
        self.wpm = None
        self.adj_wpm = None
        # ---------- Title Label ----------- #
        self.title_label = Label(self.root, text='Test Your Type', font=('Calibri', 24, 'bold'),
                                 bg=LIGHT_BLUE, fg=SUNSET_RED)
        self.title_label.grid(column=0, row=0, columnspan=2)
        # ----------- Target (Sample) Label Box ----------- #
        self.target_text = self.random_text()
        self.target_label = Label(self.root, padx=5, pady=10, text=self.target_text, font=('calibri', 16),
                                  wraplength=500, justify='center', relief=RAISED)
        self.target_label.grid(column=0, row=1, columnspan=2)
        # ---------- Instructions Label --------- #
        self.instructions = Label(self.root, padx=5, pady=10, text='Press any key to start the timer and begin typing',
                                  bg=LIGHT_BLUE, font=('calibri', 18, 'bold'))
        self.instructions.grid(column=0, row=2, columnspan=2)
        # ----- Text Input Box ------- #
        self.type_entry = Text(self.root, padx=5, pady=10, font=('Helvetica', 14, 'bold'), width=45, height=8,
                               wrap=WORD)
        self.type_entry.grid(column=0, row=3, columnspan=2)
        self.type_entry.bind('<KeyRelease>', self.start)
        # ------- WPM Labels ----- #
        self.wpm_label = Label(self.root, padx=5, pady=10, text='WPM:   ', font=('Helvetic', 14, 'bold'))
        self.wpm_label.grid(column=0, row=4)
        self.adj_wpm_label = Label(self.root, padx=5, pady=10, text='Adjusted WPM:   ', font=('Helvetic', 14, 'bold'))
        self.adj_wpm_label.grid(column=1, row=4)
        # ------- Errors Label ------ #
        self.errors_label = Label(self.root, padx=5, pady=10, text=f'Errors:', font=('Helvetic', 14, 'bold'), fg='red')
        self.errors_label.grid(column=0, row=5)
        # -------- Buttons -------- #
        self.reset_btn = Button(self.root, text='Reset', command=self.reset_text, padx=25, pady=15, bg=CORAL_ORANGE,
                                font=('Helvetic', 14, 'bold'))
        self.reset_btn.grid(column=0, row=6, padx=25, pady=10)
        self.quit_btn = Button(self.root, text='Quit', command=self.root.quit, padx=25, pady=15, bg=CORAL_ORANGE,
                               font=('Helvetic', 14, 'bold'))
        self.quit_btn.grid(column=1, row=6)
        # self.check_btn = Button(self.root, text='Check', command=self.check_errors)
        # self.check_btn.grid(column=0, row=7)

        self.errors = {}
        self.errors_text = ''
        self.root.mainloop()

    def random_text(self):
        with open('Top_1000_words.txt') as text:
            word_list = text.readlines()
        clean_list = [word.strip() for word in word_list]
        random_words = [random.choice(clean_list) for word in clean_list[:30]]
        target_text = ' '.join(random_words)
        return target_text

    def reset_text(self):
        self.running = False
        self.target_label.config(text=self.random_text())
        self.type_entry.delete('1.0', 'end')
        self.errors = {}
        self.errors_text = ''

    def check_errors(self):
        type_entry = self.type_entry.get(1.0, 'end-1c') # 'get' method for Text>> 'end-1c' to remove the space at end
        entry_words = ''.join(type_entry).split() # compile individual characters into list of words
        target_text = ''.join(self.target_label.cget('text')).split() # use cget method for Labels
        for i, word in enumerate(target_text[:len(entry_words)]): # use len(entry_words) to account for different idx
            if entry_words[i] != word:
                self.errors[word] = entry_words[i] # this will allow us to identify where we made mistakes
        for error in self.errors:
            self.errors_text += f'The word was "{error}", you wrote "{self.errors[error]}"\n'

    # this function will run every time a key is released, which bypasses the need to use while loop (crashes program)
    def start(self, event):
        self.check_finished()
        if not self.running:
            self.running = True
            self.start_time = time.time()
            print("time has started")
        entry_chars = self.type_entry.get(1.0, 'end-1c')
        entry_words = ''.join(entry_chars).split()
        target_text = ''.join(self.target_label.cget('text')).split()
        for i, word in enumerate(target_text[:len(entry_words)]): # use len(entry_words) to account for different idx
            if not word.startswith(entry_words[i]):
                self.type_entry.config(fg='red')
            else:
                self.type_entry.config(fg='green')

    def check_finished(self):
        entry_chars = self.type_entry.get(1.0, 'end-1c')
        entry_words = ''.join(entry_chars).split()
        target_text = ''.join(self.target_label.cget('text')).split()

        if len(entry_words) == 30 and len(entry_words[-1]) == len(target_text[-1]):
            self.end_time = time.time()
            print('completed typing test')
            self.total_time = self.end_time - self.start_time
            self.check_errors()
            self.wpm = round(30 / self.total_time * 60)
            self.adj_wpm = round((len(entry_chars) / self.total_time * 60) / 5)
            self.wpm_label.config(text=f'WPM: {self.wpm}')
            self.adj_wpm_label.config(text=f'Adjusted WPM: {self.adj_wpm}')
            self.errors_label.config(text=self.errors_text)
