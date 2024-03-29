import os
import logging
from main import list_stringify_scores
from main import process
from main import write_data_to_file

logger = logging.getLogger('L1J_EFL_Measures')

def main(input_path, output_file, language):
    progress_bar.config(text="Processing")
    input_filepath = os.path.join(os.getcwd(), input_path)

    scores = []
    for fdx, filename in enumerate(os.listdir(input_filepath)):
        if filename.endswith('.txt'):
            result = process(os.path.join(input_filepath, filename), filename, language)
            progress_bar.config(text=f"Processing file {filename}")
            scores.append(result)

    string_scores = list_stringify_scores(scores)
    write_data_to_file(string_scores, output_file)
    progress_bar.config(text="Files processed successfully.")


import tkinter
from tkinter import filedialog
from PIL import Image, ImageTk
m = tkinter.Tk()
m.title('Event Conflation Finder')
m.minsize(800, 660)
m.maxsize(800, 660)

input_p = tkinter.StringVar()
output_p = tkinter.StringVar()
output_f = tkinter.StringVar()
gengo = tkinter.IntVar()

def browse_input_folder():
    filepath = filedialog.askdirectory()
    input_p.set(filepath)

def browse_output_folder():
    filepath = filedialog.askdirectory()
    output_p.set(filepath)

def doit():
    lng = gengo.get()
    input_path = input_p.get()
    output_path = output_p.get()
    filename = output_f.get()
    if filename == "":
        filename = "results"
    the_thing = os.path.join(output_path, filename + '.txt')
    if lng == 2:
        language_choice = "Japanese"
    else:
        language_choice = "English"

    main(input_path, the_thing, language_choice)


def change_le():
    llabel.config(text="Select Language: ")
    input_label1.config(text='Input Path for Folder Where Text Files Are Stored:')
    input_button.config(text='Select Path')
    output_label.config(text='Where you want the file to be written:')
    output_button.config(text='Select Path')
    explanation.config(text='Do not add a file extension or path - just the name of the file. If no name is provided, the name "results" will autoamtically be selected. Caution: If any file with the name currently exists, it will be overwritten.')
    name_lbl.config(text='File Name:')
    pro_button.config(text='Process Texts Now')

def change_lj():
    llabel.config(text="言語設定：")
    input_label1.config(text='テキストファイルが入っているフォルダー:')
    input_button.config(text='参照')
    output_label.config(text='出力ファイル先：')
    output_button.config(text='参照')
    explanation.config(text='アドレスやファイル拡張子を書かずに、ファイル名だけを入力してください。名前を入力しない場合、出力ファイルは「results」という名前をつけます。＊注意＊同じアドレスに同じ名前のファイルがすでに存在している場合は上書きされます。')
    name_lbl.config(text='ファイル名')
    pro_button.config(text='開始')

bigframe = tkinter.Frame(m)
logo = Image.open("Logo.jpg")
logoimg = ImageTk.PhotoImage(logo)
logo_label = tkinter.Label(m, image=logoimg)
logo_label.image = logoimg
logo_label.pack(side=tkinter.TOP)

language_frame = tkinter.Frame(m)
lsub = tkinter.Frame(language_frame)
llabel = tkinter.Label(lsub, text="Select Language: ", font=("Times New Roman", 12))
llabel.pack(padx=10, side=tkinter.LEFT)
R1 = tkinter.Radiobutton(lsub, text="English", font=("Times New Roman", 11), variable=gengo, value=1, command=change_le)
R1.pack(padx=10, side=tkinter.LEFT)
R2 = tkinter.Radiobutton(lsub, text="日本語", font=("Times New Roman", 11), variable=gengo, value=2, command=change_lj)
R2.pack(padx=10, side=tkinter.LEFT)
lsub.pack(in_=language_frame, anchor="c")
language_frame.pack(pady=5)

input_frame = tkinter.Frame(bigframe, highlightbackground="black", highlightthickness=2, padx=10, pady=10)
input_label1 = tkinter.Label(input_frame, text='Input Path for Folder Where Text Files Are Stored:', font=("Times New Roman", 14))
input_label1.pack(side=tkinter.TOP)
entry_input = tkinter.Entry(input_frame, textvariable=input_p, width=100, highlightthickness=2, highlightcolor="light blue")
entry_input.pack(pady=5)
input_button = tkinter.Button(input_frame, text='Select Path', font=("Helvetica", 14), width=12, background="#DAF5AC", command=browse_input_folder)
input_button.pack()
input_frame.pack(pady=5)

output_frame = tkinter.Frame(bigframe, highlightbackground="black", highlightthickness=2, padx=5, pady=10)
output_label = tkinter.Label(output_frame, text='Where you want the file to be written:', font=("Times New Roman", 14))
output_label.pack(side=tkinter.TOP)
entry_output = tkinter.Entry(output_frame, textvariable=output_p, width=100, highlightthickness=2, highlightcolor="light blue")
entry_output.pack(pady=5)
output_button = tkinter.Button(output_frame, text='Select Path', font=("Helvetica", 14), width=12, background="#DAF5AC", command=browse_output_folder)
output_button.pack()
output_frame.pack(padx=10, pady=10)

name_frame = tkinter.Frame(bigframe, highlightbackground="black", highlightthickness=2, padx=5, pady=10)
explanation = tkinter.Label(name_frame, text='Do not add a file extension or path - just the name of the file. If no name is provided, the name "results" will autoamtically be selected. Caution: If any file with the name currently exists, it will be overwritten.', font=("Times New Roman", 10), justify=tkinter.LEFT, wraplength=600, width=100)
explanation.pack(side=tkinter.TOP)
subframe = tkinter.Frame(name_frame)
subframe.pack(in_=name_frame, anchor="c")
name_lbl = tkinter.Label(subframe, text='File Name:', font=("Times New Roman", 14))
name_lbl.pack(padx=5, pady=5, side=tkinter.LEFT)
entry_filename = tkinter.Entry(subframe, textvariable=output_f, width=50, highlightthickness=2, highlightcolor="light blue")
entry_filename.pack(padx=5, pady=5, side=tkinter.LEFT)
name_frame.pack(padx=10, pady=10)

pro_button = tkinter.Button(bigframe, text='Process Texts Now', font=("Helvetica", 18), width=15, background="#F75538", command=doit)
pro_button.pack(side=tkinter.BOTTOM)

bigframe.pack()

progress_bar = tkinter.Label(m, text=" ")
progress_bar.pack()

m.mainloop()
