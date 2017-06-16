import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import time

class uploadfileApp(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        # self.master.title("File Upload Assistant")
        # self.master.resizable(False, False)
        # self.master.tk_setPalette(background='#e6e6e6')
        #
        # self.master.protocol('WM_DELETE_WINDOW', self.click_cancel)
        # self.master.bind('<Escape>', self.click_cancel)

        # x = 300#(self.master.winfo_screenwidth() - self.master.winfo_reqwidth()) / 2
        # y = 250#(self.master.winfo_screenheight() - self.master.winfo_reqheight()) / 3
        # self.master.geometry("+{}+{}".format(x, y))

        # self.master.config(menu=tk.Menu(self.master))
        self.grid()
        self.pack()
        # tk.Label(self, text="This is a listbox").pack()
        self.selected_files = tuple()
        self.file_count = tk.StringVar(value='')

        # file_frame = tk.Frame(self)
        # file_frame.pack(padx=15, pady=(15, 0), anchor='w')

        self.file_button = tk.Button(self, text='Upload file(s)...', command=self.file_picker)
        self.file_button.pack(anchor='w')

        self.scrollbar_V = tk.Scrollbar(self, orient="vertical")
        self.scrollbar_H = tk.Scrollbar(self, orient="horizontal")
        self.scrollbar_V.pack(side='right', fill='y')
        self.scrollbar_H.pack(side='bottom', fill='x')
        self.listbox = tk.Listbox(self, width=50, height=15, selectmode='extended', bg='white')
        self.listbox.pack(side='left', fill='both')
        self.listbox.config(xscrollcommand=self.scrollbar_H.set)
        self.listbox.config(yscrollcommand=self.scrollbar_V.set)
        self.scrollbar_H.config(command=self.listbox.xview)
        self.scrollbar_V.config(command=self.listbox.yview)


        # self.file_label = tk.Label(file_frame, textvariable=self.file_count, anchor='e')
        # self.file_label.pack(side='right')
        #
        # tk.Label(self, text="Add a comment:").pack(padx=15, pady=(15, 0), anchor='w')

        # text_frame = tk.Frame(self, borderwidth=1, relief='sunken')
        # text_frame.pack(padx=15, pady=15)
        #
        # self.text = tk.Text(text_frame, width=30, height=4, highlightbackground='#ffffff', highlightcolor="#7baedc",
        #                     bg='#ffffff', wrap=tk.WORD, font=("System", 14))
        # self.text.focus_set()
        # self.text.pack()

        # button_frame = tk.Frame(self)
        # button_frame.pack(padx=15, pady=(0, 15), anchor='e')

        # self.submit_button = tk.Button(self, text='Submit', default='active', command=self.click_submit)
        # self.submit_button.pack(side='bottom')
        #
        # self.cancel_button = tk.Button(self, text='Cancel', command=self.click_cancel)
        # self.cancel_button.pack(side='bottom')

    def file_picker(self):
        self.selected_files = filedialog.askopenfilenames(parent=self)
        self.file_count.set('{} file(s)'.format(len(self.selected_files)))
        for l in self.selected_files:
            self.listbox.insert('end', l)

    def click_submit(self, event=None):
        print("The user clicked 'OK'")
        # comment = self.text.get('1.0', 'end')

        # if comment.rstrip():
        #     print('The user entered a comment:')
        #     print(comment.rstrip())

        if self.selected_files:
            loading = LoadingFrame(self.master, len(self.selected_files))
            # self._toggle_state('disabled')
            print('The user has selected files:')
            for path in self.selected_files:
                loading.progress['value'] += 1
                self.update()
                print('File {}/{}'.format(loading.progress['value'], loading.progress['maximum']))
                time.sleep(2)
                with open(path) as f:
                    print('Opened file: {}: {}'.format(path, f))

            print('Loading screen finished')
            loading.destroy()
            # self._toggle_state('normal')

    def click_cancel(self, event=None):
        print("The user clicked 'Cancel'")
        self.master.destroy()

    def _toggle_state(self, state):
        state = state if state in ('normal', 'disabled') else 'normal'
        widgets = (self.file_button, self.file_label, self.text, self.submit_button, self.cancel_button)
        for widget in widgets:
            widget.configure(state=state)


class LoadingFrame(tk.Frame):
    def __init__(self, master, count):
        tk.Frame.__init__(self, master, borderwidth=5, relief='groove')
        self.grid(row=0, column=0)

        tk.Label(self, text="Your files are being uploaded").pack(padx=15, pady=10)

        self.progress = ttk.Progressbar(self, orient='horizontal', length=250, mode='determinate')
        self.progress.pack(padx=15, pady=10)
        self.progress['value'] = 0
        self.progress['maximum'] = count