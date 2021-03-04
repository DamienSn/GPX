import bs4
import re
import os
import sys
import datetime
from tkinter import *
from tkinter import filedialog
from tkinter.ttk import Treeview
import tkinter.messagebox


class App:
    def __init__(self):
        self.window = Tk()
        self.window.title('GPX Hour')
        self.window.geometry('300x250')
        self.window.iconbitmap('.ico\\logo.ico')

    def create_widgets(self):
        self.title = Label(self.window, text="GPX Hour", font=["Arial", 25])
        self.title.pack()

        self.browse_btn = Button(
            self.window, text="Open file", command=self.browse)
        self.browse_btn.pack()

        self.file_label = Label(self.window, text="No file opened")
        self.file_label.pack()

        Label(self.window, text='Start time (yyyy-mm-dd hh-mm-ss)').pack()

        self.entry1 = Entry(self.window)
        self.entry1.pack()
        self.entry1.name = "start hour"

        Label(self.window, text='Finish time (yyyy-mm-dd hh-mm-ss)').pack()

        self.entry2 = Entry(self.window)
        self.entry2.pack()
        self.entry2.name = "finish hour"

        self.process_btn = Button(self.window, text="Process", command=self.process, state=DISABLED)
        self.process_btn.pack()

        self.output_label = Label(self.window, text="")
        self.output_label.pack()

    def browse(self):
        file = filedialog.askopenfilename(
            title="Select A File", filetype=[("GPX files", "*.gpx")])

        if file:
            self.file = file
            self.fname = self.file.split('/')
            self.fname = self.fname[len(self.fname) - 1]
            self.file_url = self.file.replace(self.fname, '')
            self.process_btn.config(state=ACTIVE)
            self.file_label.config(text=f'File : {self.fname}')

    def process(self):
        with open(self.file, 'r') as f:
            xml = f.read()
            bx = bs4.BeautifulSoup(xml, 'lxml-xml')
            times = bx.find_all('time')
            s1 = self.get_entry(self.entry1)
            s2 = self.get_entry(self.entry2)
            dx = datetime.datetime.strptime(s1, '%Y-%m-%dT%H:%M:%SZ')
            dy = datetime.datetime.strptime(s2, '%Y-%m-%dT%H:%M:%SZ')
            tdeltax = dy - dx
            tdeltay = tdeltax/(len(times)-2)
            print(tdeltay*(len(times) - 2))
            print(tdeltay)
        
            for index, time in enumerate(times):
                timestr = time.text
                if index == 0:
                    time.string.replace_with(s1)
                elif index > 0 and index < (len(times) - 1):
                    dt = datetime.datetime.strptime(s1, '%Y-%m-%dT%H:%M:%SZ')
                    dt += tdeltay * index
                    time.string.replace_with(dt.strftime('%Y-%m-%dT%H:%M:%SZ'))
                elif index == (len(times) - 1):
                    time.string.replace_with(s2)

            new_file = self.fname.split('.gpx')[0] + '_modified.gpx'
            with open(self.file_url + new_file, 'w') as g:
                g.write(bx.prettify())
                self.output_label.config(text=f'Output file : {new_file}')

    def get_entry(self, entry):
        val = entry.get()
        regex = r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}'

        if re.match(regex, val):
            re1 = re.compile(r'\d{4}-\d{2}-\d{2}')
            re2 = re.compile(r'\d{2}:\d{2}:\d{2}')

            splited = val.split(' ')
            val = splited[0] + 'T' + splited[1] + 'Z'
            
            return(val)
        else:
            tkinter.messagebox.showerror(title='Invalid value', message=f'The value that you have entered on the entry {entry.name} is invalid. Please respect the format.')

    def start(self):
        self.window.mainloop()


app = App()
app.create_widgets()
app.start()
