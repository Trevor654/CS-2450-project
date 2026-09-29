from tkinter import *
from tkinter import filedialog

root = Tk()
root.title("GUI test")
# root.iconbitmap("folder/image.ico")
root.geometry('600x400')

def hide_home():
    # my_label.config(text="new text")
    
    #The following 2 lines hide the old home screen
    welcome_label.pack_forget()
    file_upload_button.pack_forget()
    my_button.pack_forget()

    # after hiding the old home screen it loads the new screen
    load_page_2()


def load_page_2():
    output_box.grid(row=0,column=0,columnspan=2)
    run_button.grid(row=1,column=0)
    back_button.grid(row=2,column=0)
    input_field_text.grid(row=1,column=1)
    input_field.grid(row=2,column=1,ipady=10)

def show_home():
    # Should figure out how to restore it to exactly how it was without manually adding everything the same way
    output_box.grid_forget()
    run_button.grid_forget()
    back_button.grid_forget()
    input_field.grid_forget()
    input_field_text.grid_forget()


    
    welcome_label.pack(pady=20)
    file_upload_button.pack(pady=20)
    my_button.pack(pady=20)
    
    # my_button2.pack(pady=20)

def run():
    pass

def file_select():
    root.filename = filedialog.askopenfilename(title="Select a file",initialdir='/',filetypes=[('txt files', '*.txt')])
    print(root.filename)

#Create a label
welcome_label = Label(root, text="Welcome to da program", font=("Helvetica", 36))
welcome_label.pack(pady=20)

#Pack, Grid, Placel
# my_label.grid()
my_button = Button(root, text="Next page", command=hide_home)
my_button.pack(pady=20)

file_upload_button = Button(root, text='Open File', command=file_select)
file_upload_button.pack(pady=20)
# file_upload_button.pack(pady=20)

#page 2 labels
output_box = Label(root, text="Output will be put here", bg="yellow", bd=20, height=10, width=63, padx=5, pady=5)
run_button = Button(root, text="Run", command=run, height=3, width=15)
back_button = Button(root, text="Go back", command=show_home, height=3, width=15)
input_field_text = Label(root, text="When needed, please input text in the box under this text")
input_field = Entry(root, width=30, font=('Arial', 14))
# my_button2.pack(pady=20)

root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.columnconfigure(2, weight=1)
root.columnconfigure(3, weight=1)

root.mainloop()
