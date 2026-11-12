import multiprocessing
from tkinter import *
from tkinter import filedialog
from tkinter import colorchooser
from functions import *

class Gui:
    def __init__(self, cpu_class=None):

        #General GUI setup
        self.root = Tk()
        self.root.title("UV Simulator")
        self.root.geometry('550x400')

        #variables to help with cpu
        self.cpu_class = cpu_class
        self.created_cpu = None
        self.file_path = None
        self.pointer = 0
        
        #Set colors for things
        self.primary_color = "#4C721D"
        self.off_color = "#FFFFFF"
        self.root.configure(bg=self.primary_color)

        #setup

        #Color picker buttons
        self.primary_color_picker = Button(self.root, text="Primary color", bg=self.off_color, height=1, width=13, command=self.primary_color_change)
        self.off_color_picker = Button(self.root, text="Off color", bg=self.off_color, height=1, width=13, command=self.off_color_change)
        self.new_window_button = Button(self.root, text="New Window", bg=self.off_color, height=1, command=self.new_window)

        #Ouput box and children
        self.output_box_margin = Label(self.root, bg=self.primary_color, pady=10, padx=10, width=190)
        self.output_box = Label(self.output_box_margin, bg=self.off_color, height=10, width=130, pady=10)        #Parent for output_box_text and error_text
        self.output_box_text = Text(self.output_box, bg=self.off_color, bd=0, height=10, width=130, state="disabled", font=("Arial", 10))
        self.error_text = Label(self.output_box, text=" ", fg="red", bg=self.off_color, height=1, width=50, font=("Arial", 10))

        #Row 2
        self.file_upload_button = Button(self.root, text="Open File", bg=self.off_color, height=2, width=13, command=self.file_select)
        self.run_button = Button(self.root, text="Run", bg=self.off_color, height=2, width=13, state='disabled', command=self.gui_run_setup)

        #Row 3
        self.edit_file_button = Button(self.root, text="Edit File", bg=self.off_color, height=2, width=13, state='disabled', command=self.open_editor)
        self.reset_button = Button(self.root, text="Reset", bg=self.off_color, height=2, width=13, state='disabled', command=self.gui_reset)

        #Input related buttons and fields
        self.input_field_text = Label(self.root, text="When needed, input text in the box below",font=('Arial', 8), width=36, bg=self.off_color)
        self.input_field = Entry(self.root, width=24, font=('Arial', 13), state="disabled", bg=self.off_color, disabledbackground=self.off_color)
        self.enter_value = Button(self.root, text="Enter", font=('Arial', 13), width=6, height=1, state="disabled", bg=self.off_color, command=self.get_input)

        #Setup for color changer
        self.primary_color_items = [self.root,self.output_box_margin]
        self.off_color_items = [
                                self.primary_color_picker,self.off_color_picker,self.new_window_button,
                                self.output_box,self.output_box_text,self.error_text,
                                self.file_upload_button,self.run_button,self.input_field_text,
                                self.edit_file_button,self.reset_button,self.input_field,self.enter_value,
                                ]

        #Welcome to program text
        self.output_box_text.config(state="normal")
        self.output_box_text.insert("end", "Welcome to the program\n")
        self.output_box_text.see("end")
        self.output_box_text.config(state="disabled")

        #Put the gui objects on the gui
        self.setup_gui_display()

        #Formating to center things
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.columnconfigure(2, weight=0)
        self.root.columnconfigure(3, weight=0)

        #Allows the thing to close
        self.root.mainloop()
    
    #display classes

    def new_window(self):
        multiprocessing.get_context('spawn').Process(target=Gui, args=(self.cpu_class,)).start()

    def setup_gui_display(self):

        #Color change buttons
        self.primary_color_picker.grid(row=0,column=0,padx=(10,0))
        self.off_color_picker.grid(row=0,column=1)
        self.new_window_button.grid(row=0,column=4,padx=(145,0))

        #Output box and children
        self.output_box_margin.grid(row=1,columnspan=5,pady=10,padx=(10,10))     #provides a nice looking margin
        self.output_box.grid(row=1,column=0,columnspan=5)
        self.output_box_text.grid(row=1,column=0,columnspan=5)
        self.error_text.grid(row=2,column=0,columnspan=2,padx=(0,10))

        #Row 2
        self.file_upload_button.grid(row=2,column=0,padx=(10,0))
        self.run_button.grid(row=2,column=1)

        #Row 3
        self.edit_file_button.grid(row=3,column=0,padx=(10,0))
        self.reset_button.grid(row=3,column=1)
        
        #Input field buttons
        self.input_field_text.grid(row=2,column=2,columnspan=3,padx=(10,10))
        self.input_field.grid(row=3,column=2,ipady=7,columnspan=3,padx=(10,10))
        self.enter_value.grid(row=3,column=4,padx=(160,0))

    #user input classes
    def file_select(self):
        self.root.filename = filedialog.askopenfilename(title="Select a file",initialdir='/',filetypes=[('txt files', '*.txt')])
        try:
            if self.root.filename == '':
                raise FileNotFoundError("Please select a file")
            #Edit is allowed even if the file is malformed, so the user can fix it
            self.file_path = self.root.filename
            self.edit_file_button.config(state='normal')
            self.run_button.config(state='disabled')
            self.created_cpu = self.cpu_class(self.root.filename, self)
            self.run_button.config(state='normal')
        except Exception as e:
            self.print_error(e)
            print(e)

    def get_input(self):
        the_input = self.input_field.get()
        self.input_field_text.config(fg="black")

        try:
            the_input = convertNumToCommand(the_input, self.created_cpu._fileFormat)
        except:
            self.input_field_text.config(fg="red")
            return
        self.gui_run(self.pointer,the_input)

    #general gui classes
    def gui_run_setup(self):
        #stops the run button from being pressed while a file is being read
        self.run_button.config(state='disabled')   

        #creates a new cpu each time the function runs
        self.created_cpu = self.cpu_class(self.file_path, self)
        self.gui_run()

    def gui_run(self, pointer_int=0, input_recieved=''):

        #sets the pointer if one is given (used when getting input from user)
        self.pointer = pointer_int 

        #Sets fields to reset after recieving input
        self.change_input_label("When needed, input text in the box below")
        self.input_field.delete(0, 'end')
        self.input_field.config(state='disabled')
        self.enter_value.config(state='disabled')

        halted = False
        
        while not halted:
            #Recieves a tuple from the cpu run function detailing
            # (halted (boolean), pointer (int), need_input (boolean), print_val (string))
            #
            # Using that tuple it determines whether the file is done reading or not, where the pointer is
            # for the next line to read, whether it needs to wait for input from the user, and if it does need
            # input, what to ask the user for in the label above the entry box

            # print(f' input pre check {input_recieved}')
            if input_recieved == '':
                cpu_tuple = self.created_cpu.run(self.pointer)
                # print(f'got no input')
            else:
                cpu_tuple = self.created_cpu.run(self.pointer,input_recieved)
                # print(f'got {input_recieved}')
                input_recieved = ''
            # print(cpu_tuple)
            halted = cpu_tuple[0]
            self.pointer = cpu_tuple[1]
            need_input = cpu_tuple[2]
            print_val = cpu_tuple[3]

            if need_input == True:
                # sets the input field and enter button to active and makes the program wait for input before continuing
                self.change_input_label(print_val)
                # self.input_field.config(bg="yellow")
                self.input_field.config(state='normal')
                self.enter_value.config(state='normal')
                break

            if halted == True:
                self.reset_button.config(state='normal')

    def gui_reset(self):
        self.run_button.config(state="normal")
        self.output_box_text.config(state="normal")
        self.output_box_text.delete("1.0","end")
        self.output_box_text.config(state="disabled")
        self.error_text.config(text=' ')

    def open_editor(self):
        #Second window for reading and editing the loaded file
        self.editor_window = Toplevel(self.root)
        self.editor_window.title("Edit File")
        self.editor_window.configure(bg=self.primary_color)

        self.editor_text = Text(self.editor_window, bg=self.off_color, height=20, width=30, font=("Arial", 10))
        self.editor_text.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        with open(self.file_path, 'r') as file:
            self.editor_text.insert("1.0", file.read())

        self.save_button = Button(self.editor_window, text="Save", bg=self.off_color, height=1, width=10, command=self.save_file)
        self.save_button.grid(row=1, column=0, pady=(0, 10))
        self.save_as_button = Button(self.editor_window, text="Save As", bg=self.off_color, height=1, width=10, command=self.save_as_file)
        self.save_as_button.grid(row=1, column=1, pady=(0, 10))

    def over_max_size(self):
        #Memory only has 250 spots (000 - 249)
        if len(self.editor_text.get("1.0", "end-1c").split('\n')) > self.created_cpu.maxFileSize:
            self.print_error(f"Error: can't save, over max size of {self.created_cpu.maxFileSize} entries")
            return True
        return False

    def save_file(self):
        if self.over_max_size():
            return

        #"end-1c" leaves off the extra newline
        with open(self.file_path, 'w') as file:
            file.write(self.editor_text.get("1.0", "end-1c"))

        #Reload the file so that gets checked and keep the window open if error
        try:
            self.created_cpu = self.cpu_class(self.file_path, self)
            self.print_error(' ')
            self.run_button.config(state='normal')
            self.editor_window.destroy()
        except Exception as e:
            self.run_button.config(state='disabled')
            self.print_error(e)

    def save_as_file(self):
        #Lets the usr pick a new name and folder then saves there and uses that file from now on
        if self.over_max_size():
            return
        new_path = filedialog.asksaveasfilename(parent=self.editor_window, title="Save file as", defaultextension=".txt", filetypes=[('txt files', '*.txt')])
        if not new_path:
            return
        self.file_path = new_path
        self.save_file()

    def primary_color_change(self):
        new_color = colorchooser.askcolor()
        self.primary_color = new_color[1]
        for item in self.primary_color_items:
            item.configure(bg=self.primary_color)

        if hasattr(self, "editor_window") and self.editor_window.winfo_exists():
            self.editor_window.configure(bg=self.primary_color)

    def off_color_change(self):
        new_color = colorchooser.askcolor()
        self.off_color = new_color[1]
        self.input_field.configure(disabledbackground=self.off_color)
        for item in self.off_color_items:
            item.configure(bg=self.off_color)

        if hasattr(self, "editor_window") and self.editor_window.winfo_exists():
            self.editor_text.configure(bg=self.off_color)
            self.save_button.configure(bg=self.off_color)
            self.save_as_button.configure(bg=self.off_color)

    #output classes
    def change_input_label(self,output_text):
        self.input_field_text.config(text=output_text)

    def print_output(self, output_text):
        self.output_box_text.config(state="normal")
        self.output_box_text.insert("end", str(output_text) + "\n")
        self.output_box_text.see("end")
        self.output_box_text.config(state="disabled")
            
    def print_error(self, error_msg):
        self.error_text.config(text=error_msg)

if __name__ == '__main__':
    Gui()
