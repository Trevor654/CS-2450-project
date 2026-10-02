from tkinter import *
from tkinter import filedialog

class Gui:
    def __init__(self, cpu_class=None):

        #General GUI setup
        self.root = Tk()
        self.root.title("GUI test")
        self.root.geometry('510x400')
        # root.iconbitmap("folder/image.ico")

        #variables to help with cpu
        self.cpu_class = cpu_class
        self.created_cpu = None
        self.pointer = 0

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
        self.output_box = Label(self.root, text="Output will be put here", bg="yellow", bd=5, height=10, width=63, padx=20, pady=10)
        self.run_button = Button(self.root, text="Run", command=self.run_setup, height=3, width=15)
        self.back_button = Button(self.root, text="Go back", command=self.show_home, height=3, width=15)
        self.input_field_text = Label(self.root, text="When needed, please input text in the box under this text")
        self.input_field = Entry(self.root, width=24, font=('Arial', 14), state="disabled")
        self.enter_value = Button(self.root, text="Enter", command=self.get_input, width=7, height=2, state="disabled")

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
        self.output_box.grid(row=0,column=0,columnspan=3)
        self.run_button.grid(row=1,column=0)
        self.back_button.grid(row=2,column=0)
        self.input_field_text.grid(row=1,column=1,columnspan=2)
        self.input_field.grid(row=2,column=1,ipady=10)
        self.enter_value.grid(row=2,column=2)

    def show_home(self):

        #Hide all the page 2 items
        self.output_box.grid_forget()
        self.run_button.grid_forget()
        self.back_button.grid_forget()
        self.input_field.grid_forget()
        self.input_field_text.grid_forget()
        self.enter_value.grid_forget()

        self.run_button.config(state='normal')
        self.input_field.config(state='normal')
        self.input_field.delete(0, 'end')
        self.input_field.config(state='disabled')

        #Unhide the page 1 items
        self.welcome_label.pack(pady=20)
        self.file_upload_button.pack(pady=20)
        self.next_button.pack(pady=20)
        
    def file_select(self):
        self.root.filename = filedialog.askopenfilename(title="Select a file",initialdir='/',filetypes=[('txt files', '*.txt')])
        print(self.root.filename)
        self.created_cpu = self.cpu_class(self.root.filename)
        try:
            self.created_cpu = self.cpu_class(self.root.filename)
            self.hide_home()
        except:
            print('No file selected')

    def get_input(self):
        the_input = self.input_field.get()
        self.gui_run(self.pointer,the_input)
        
        # print(my_variable)

    def run_setup(self):
        self.run_button.config(state='disabled')
        self.gui_run()
        
    def gui_run(self, pointer_int=0, input_recieved=''):
        if self.cpu_class != None:
            # self.created_cpu.run()
            # print(self.created_cpu.run())
            self.pointer = pointer_int
            halted = False

            self.change_input_label("When needed, please input text in the box under this text")
            self.input_field.delete(0, 'end')
            self.input_field.config(state='disabled')
            self.enter_value.config(state='disabled')

            while not halted:
                cpu_tuple = self.created_cpu.run(self.pointer,input_recieved)
                # print(cpu_tuple)
                halted = cpu_tuple[0]
                self.pointer = cpu_tuple[1]
                need_input = cpu_tuple[2]
                print_val = cpu_tuple[3]
                # self.print_ouput(print_val)

                if need_input == True:
                    self.change_input_label(print_val)
                    self.input_field.config(bg="yellow")
                    self.input_field.config(state='normal')
                    self.enter_value.config(state='normal')
                    break

                # self.print_ouput(str(cpu_tuple))
                # print(halted)


    def print_ouput(self,output_text):
        self.output_box.config(text=output_text)

    def change_input_label(self,output_text):
        self.input_field_text.config(text=output_text)
    
    def print_error(self, error_msg):
        self.error_text.config(text=error_msg)
        self.error_text.pack()

if __name__ == '__main__':
    Gui()
