from tkinter import *
from tkinter import filedialog


class Gui:
    def __init__(self):

        #General GUI setup
        self.root = Tk()
        self.root.title("GUI test")
        self.root.geometry('510x400')
        # root.iconbitmap("folder/image.ico")

        #Welcome label & homepage
        self.welcome_label = Label(self.root, text="Welcome to da program", font=("Helvetica", 34))
        self.welcome_label.pack(pady=20)

        self.file_upload_button = Button(self.root, text='Open File', command=self.file_select, width=32, height=7, bd=6)
        self.file_upload_button.pack(pady=20)

        self.next_button = Button(self.root, text="Next page", command=self.hide_home)
        self.next_button.pack(pady=20)

        #page 1 error text
        self.error_text = Label(self.root, text="error", fg="red")

        #page 2 labels
        self.output_box = Label(self.root, text="Output will be put here", bg="yellow", bd=5, height=10, width=60, padx=20, pady=10)
        self.run_button = Button(self.root, text="Run", command=self.run, height=3, width=15)
        self.back_button = Button(self.root, text="Go back", command=self.show_home, height=3, width=15)
        self.input_field_text = Label(self.root, text="When needed, please input text in the box under this text")
        self.input_field = Entry(self.root, width=30, font=('Arial', 14))

        #Formating to center page 2 stuff
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.columnconfigure(2, weight=1)

        #Allows the thing to close
        self.root.mainloop()


    def hide_home(self):

        #Hides the home screen
        self.welcome_label.pack_forget()
        self.file_upload_button.pack_forget()
        self.next_button.pack_forget()

        #Unhides page 2
        self.output_box.grid(row=0,column=0,columnspan=2)
        self.run_button.grid(row=1,column=0)
        self.back_button.grid(row=2,column=0)
        self.input_field_text.grid(row=1,column=1)
        self.input_field.grid(row=2,column=1,ipady=10)

    def show_home(self):

        #Hide all the page 2 items
        self.output_box.grid_forget()
        self.run_button.grid_forget()
        self.back_button.grid_forget()
        self.input_field.grid_forget()
        self.input_field_text.grid_forget()

        #Unhide the page 1 items
        self.welcome_label.pack(pady=20)
        self.file_upload_button.pack(pady=20)
        self.next_button.pack(pady=20)
        
    def file_select(self):
        self.root.filename = filedialog.askopenfilename(title="Select a file",initialdir='/',filetypes=[('txt files', '*.txt')])
        print(self.root.filename)
        return self.root.filename

    def run(self):
        pass

    def print_ouput(self,output_text):
        self.output_box.config(text=output_text)
    
    def print_error(self, error_msg):
        self.error_text.config(text=error_msg)
        self.error_text.pack()

if __name__ == '__main__':
    Gui()