import tkinter as tk
from tkinter import filedialog, Text
import os
from PIL import ImageTk, Image
import tkinter.font as tkFont

def delete_widget(widget):
    widget.destroy()

apps = []
class tkinterApp(tk.Tk):

    # __init__ function for class tkinterApp
    def __init__(self, *args, **kwargs):
        # __init__ function for class Tk
        # as it ihirit from tk.TK
        tk.Tk.__init__(self, *args, **kwargs)

        # creating a container
        #default tkinter app layout
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # initializing frames to an empty array
        self.frames = {}

        # iterating through a tuple consisting
        # of the different page layouts
        for F in (StartPage, Page1):
            frame = F(container, self)

            # initializing frame of that object from
            # startpage, page1, page2 respectively with
            # for loop
            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage) #show start page

    # to display the current frame passed as
    # parameter
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise() # to show on the top StartPage!




# first window frame startpage
class StartPage(tk.Frame):
    def __init__(self, parent, controller): #constructor of StartPage
        # self.path = path
        self.path = ""
        self.controller = controller
        #as it ihirit from tk.Frame
        tk.Frame.__init__(self, parent)
        main_frame = tk.Frame(self, bg="#9BBDF9")
        main_frame.place(relwidth=1, relheight=1, relx=0, rely=0)
        frame1 = tk.Frame(main_frame, bg="#B95F89")
        frame1.place(relwidth=0.75, relheight=0.75, relx=0.125, rely=0.125)
        screen1 = tk.Label(main_frame, text="Screen 0", fg="black", bg="#9BBDF9", font=("Times", 15))
        screen1.place(relx=0.48, rely=0.025)
        self.frame1 = frame1

        # # image use "pip install Pillow" first please
        # xml_image = Image.open("assets/xml_pic.png")
        # xml_img_resized = xml_image.resize((650, 400), Image.ANTIALIAS)
        # my_img = ImageTk.PhotoImage(xml_img_resized)
        # my_label = tk.Label(app, image=my_img)
        # my_label.place(relx=0.29, rely=0.30)

        #=======================converting image into frame_text
        s = """
<?xml version="1.0" encoding="UTF-8"?>
<users>
    <user>
        <id>1</id>
        <name>Ahmed Ali</name>
        <posts>...
        </posts>
        <followers>...
        </followers>
    </user>
    <user>
        <id>2</id>
        <name>Yasser Ahmed</name>
        <posts>
            <post>
                <body>
                    Lorem ipsum dolor sit amet
                </body>
                """
        print(s)
        frame2 = tk.Frame(main_frame, bg="#F0F0F0")
        frame2.place(relx=0.35, rely=0.3, relwidth=0.3 ,relheight=0.5)
        self.frame2 = frame2
        #Text in the Frame
        self.print_right_text(s)
        #Text
        label = tk.Label(frame1, text="Welcome To Our XML Parser\nPlease Choose The Input File", bg="#B95F89", fg="white", font=("Times", 25))
        label.place(relx=0.33, rely=0.05)

        # button
        browse = tk.Button(frame1, text="Choose xml/encoded File", font=(("Times", 15)), padx=10, pady=5, fg="white", bg="black", command=self.addApp, activebackground='#9BBDF9')
        browse.place(relheight=0.07, relx=0.4, rely=0.92)

       #path_widget
        if self.path != "":
            apps.insert(0, self.path)
            path_widget = tk.Label(frame1, text=self.path)
            path_widget.place( relx=0.62, rely=0.90)
        # next button
        next_btn = tk.Button(frame1, text="next", padx=5, pady=2.5, fg="white", bg="black", command=self.go_next, activebackground='#9BBDF9')
        next_btn.place(relx=0.9, rely=0.95)

    def addApp(self):
        for widget in self.frame1.winfo_children():
            if str(widget) == "path_widget":
                widget.destroy
        filename = filedialog.askopenfilename(initialdir="/", title="Select File", filetypes=(
        ("XML File", "*.xml"), ("Encoded Text File", "*.text"),("select all", "*.*"))
        )  # navigate from here "/" and type is xml or txt or anyfile
        f = open(filename, 'r')
        for e in f:
            apps.append(e)
            print(e)

        # remove empty spaces
        if len(filename) != 0:
            self.path = filename

        print(filename)
        if self.path != "":
            path_widget = tk.Label(self.frame1, text=self.path)
            path_widget.place(relx=0.6, rely=0.90)

    def go_next(self):
        if (self.path != ""):
            self.controller.show_frame(Page1)
        else:
            path_widget = tk.Label(self.frame1, text="Please Chose File First", fg="red")
            path_widget.place(relx=0.6, rely=0.90)

    def print_right_text(self, text):
        s = text.split('\n')
        # button1.pack(side=tkinter.LEFT)
        flag = True
        for string in s:
            if flag == True:
                flag = False
                continue
            text_widget = tk.Label(self.frame2, text=string, fg="black")
            text_widget.pack(side="top", anchor="nw")

    @staticmethod
    def paths_returner(self):
        return self.paths
    @staticmethod
    def path_returner(self):
        return self.path
#Screen 2
class Page1(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        #instance of Start page share same static method
        # s = StartPage(parent, controller).paths_returner()
        # self.path = '/'
        self.isXml = False
        print("175")
        main_frame = tk.Frame(self, bg="#9BBDF9")
        main_frame.place(relwidth=1, relheight=1, relx=0, rely=0)
        #screen 1 text
        screen1 = tk.Label(main_frame, text="Screen 1", fg="black", bg="#9BBDF9", font=("Times", 15))
        screen1.place(relx=0.48, rely=0.025)

        #left frame
        code_frame = tk.Frame(main_frame, bg="white")
        code_frame.place(relx= 0.05, rely=0.05, relwidth=0.4, relheight=0.5)
        #right frame
        result_frame = tk.Frame(main_frame, bg="white")
        result_frame.place(relx=0.55, rely=0.05, relwidth=0.4, relheight=0.5)
        #read lines from you code

        # f = open(str(self.path), 'r')
        # lines = f.read()
        # print(lines)

        # #xml file
        if "<" in apps:
            self.isXml = True
            print("197")
            for text in apps:
                code_left = tk.Label(code_frame, text)
        #encoded file
        else:
            self.isXml = False
            print("203")
            for text in apps:
                code_left = tk.Label(code_frame, text)


# Driver Code

app = tkinterApp() #equivilent to => root = tk.Tk()

#width and height of your labtop
h = app.winfo_screenheight() # Returns screen height in pixels
w = app.winfo_screenwidth() # Returns screen width in pixels
#open at largest size
app.state("zoomed")
app.minsize(height= h, width= w)

#title and icon
app.title("XML Parser")
app.iconbitmap(default=r"assets/xml-file.ico")


#fonts
font_header = tkFont.Font(family="Times", size=25)
font_body = tkFont.Font(family="Times", size=15)
font_footer = tkFont.Font(family="Times", size=15)




# canvas = tk.Canvas(app, height=h, width=w, bg="#9BBDF9")
# canvas.pack()

# # image use "pip install Pillow" first please
# xml_image = Image.open("assets/xml_pic.png")
# # # xml_image.show()
# xml_img_resized = xml_image.resize((650, 400), Image.ANTIALIAS)
# my_img = ImageTk.PhotoImage(xml_img_resized)
# my_label = tk.Label(app, image=my_img)
# my_label.place(relx=0.29, rely=0.30)



label02 = tk.Label(app, text="Made By The Parsers", bg="black", fg="white", font=("Times", 15))
label02.place(relx=0.44, rely=0.92)




app.mainloop()
