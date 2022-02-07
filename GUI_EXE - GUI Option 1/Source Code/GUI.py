import tkinter as tk
from tkinter import filedialog
from XML import *
#for ploting Graph
# import networkx as nx
from networkx import DiGraph, draw_networkx
# import matplotlib.pyplot as plt
from matplotlib.pyplot import figure, show, style, grid

# import seaborn as sns
# sns.set()
# import os
import tkinter.font as tkFont
# from tkinter import Text
# from PIL import ImageTk, Image

def delete_widget(widget):
    widget.destroy()

class tkinterApp(tk.Tk):

    # __init__ function for class tkinterApp
    def __init__(self, *args, **kwargs):
        # __init__ function for class Tk
        # as it ihirit from tk.TK
        tk.Tk.__init__(self, *args, **kwargs)
        #default tkinter app layout
        container = tk.Frame(self)
        # Initialize Window
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # initializing frames to an empty array
        self.frames = {}

        # iterating through a tuple consisting
        # of the different page layouts
        for F in (StartPage, Page1, Page2):
            frame = F(container, self)

            # initializing frame of that object from
            # startpage, page1 respectively with
            # for loop
            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage) #show start page

    # to display the current frame passed as
    # parameter
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise() # to show on the top StartPage!
        return True

    # passes text to the window StartPage
    # def pass_on_text(self, text):
    #     self.frames[StartPage].get_text(text)

    # passes text to the window Page1
    def pass_on_text2(self, text):
        self.frames[Page1].get_text(text)

    def pass_on_msg(self, msg1, msg2):
        self.frames[Page2].get_msg(msg1, msg2)

    def pass_graph(self, flag):
        self.frames[Page2].get_graph(flag)


    def destory_app(self):
        self.destroy()


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
        # print(s)
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

        # path_widget
        path_widget = tk.Label(frame1, bg="#B95F89")
        path_widget.place(relx=0.62, rely=0.90)
        self.path_widget = path_widget


        # next button
        next_btn = tk.Button(frame1, text="next", padx=5, pady=2.5, fg="white", bg="black", command=self.go_next, activebackground='#9BBDF9')
        next_btn.place(relx=0.9, rely=0.95)

    # send text to Page1
    def send_text(self, text):
        self.controller.pass_on_text2(text)

    # # get information and change the displayed text
    # def get_text(self, text):
    #     self.label.config(text=text)

    def addApp(self):
        for widget in self.frame1.winfo_children():
            if str(widget) == "path_widget":
                widget.destroy
        filename = filedialog.askopenfilename(initialdir="/", title="Select File", filetypes=(
        ("XML File", "*.xml"), ("Encoded File", "*.enc"), ("Encoded Text File", "*.txt"), ("select all", "*.*"))
        )  # navigate from here "/" and type is xml or txt or anyfile

        # remove empty spaces
        if len(filename) != 0:
            self.path = filename
            # self.send_text(self.path)

        # print(filename)
        if self.path != '':
            self.path_widget.destroy()
            path_widget = tk.Label(self.frame1, text=self.path)
            path_widget.place(relx=0.6, rely=0.90)
            self.path_widget = path_widget

    def go_next(self):
        if (self.path != ''):
            self.send_text(self.path)
            self.controller.show_frame(Page1)
        else:
            self.path_widget.destroy()
            path_widget = tk.Label(self.frame1, text="Please Chose File First", fg="red")
            path_widget.place(relx=0.6, rely=0.90)

    def print_right_text(self, text):
        s = text.split('\n')
        flag = True
        for string in s:
            if flag == True:
                flag = False
                continue
            text_widget = tk.Label(self.frame2, text=string, fg="black")
            text_widget.pack(side="top", anchor="nw")
#Screen 2
class Page1(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        #instance of Start page share same static method
        self.isXml = False
        self.controller = controller
        self.isPressed_1 = False
        self.isPressed_2 = False
        self.isPressed_3 = False
        self.isPressed_4 = False
        #XML Object
        self.XML_object = None

        main_frame = tk.Frame(self, bg="#9BBDF9")
        main_frame.place(relwidth=1, relheight=1, relx=0, rely=0)
        self.main_frame = main_frame
        #screen 1 text
        screen1 = tk.Label(main_frame, text="Screen 1", fg="black", bg="#9BBDF9", font=("Times", 15))
        screen1.place(relx=0.48, rely=0.025)

        #left frame
        code_frame = tk.Frame(main_frame, bg="#F0F0F0")
        code_frame.place(relx= 0.05, rely=0.05, relwidth=0.4, relheight=0.5)
        self.code_frame = code_frame

        #right frame
        result_frame = tk.Frame(main_frame, bg="#F0F0F0")
        result_frame.place(relx=0.55, rely=0.05, relwidth=0.4, relheight=0.5)
        self.result_frame = result_frame
        self.result_second_frame = self.result_frame

        consestancey = tk.Button(main_frame, text="Consestancey", font=(("Times", 15)), padx=10, pady=5, fg="white", bg="black", command=self.consestancy, activebackground='#9BBDF9')
        consestancey.place(relx=0.08, rely=0.6, relwidth=0.15)

        formating = tk.Button(main_frame, text="Formating", state="disabled",font=(("Times", 15)), padx=10, pady=5, fg="white", bg="black", command=self.formating, activebackground='#9BBDF9')
        formating.place(relx=0.31, rely=0.6, relwidth=0.15)
        self.formating_btn = formating

        convert = tk.Button(main_frame, text="Convert X/J", state="disabled",font=(("Times", 15)), padx=10, pady=5, fg="white", bg="black", command=self.convert, activebackground='#9BBDF9')
        convert.place(relx=0.54, rely=0.6, relwidth=0.15)
        self.convert_btn = convert

        self.codec = ""
        codec = tk.Button(self.main_frame, text=self.codec, state="disabled", font=(("Times", 15)), padx=10, pady=5, fg="white", bg="black", command=self.codec_func, activebackground='#9BBDF9')
        codec.place(relx=0.77, rely=0.6, relwidth=0.15)
        self.codec_btn = codec

        #TEXTS
        list_text = tk.Label(main_frame, text="List", fg="black", bg="#9BBDF9", font=("Times", 15))
        list_text.place(relx=0.05, rely=0.66, relheight=0.04)

        consestancey_text = tk.Label(main_frame, text="Consestancey", fg="black", bg="#9BBDF9", font=("Times", 15))
        consestancey_text.place(relx=0.05, rely=0.7, relheight=0.04)

        formating_text = tk.Label(main_frame, text="Formating", fg="black", bg="#9BBDF9", font=("Times", 15))
        formating_text.place(relx=0.05, rely=0.75, relheight=0.04)

        convert_text = tk.Label(main_frame, text="Convert X/J", fg="black", bg="#9BBDF9", font=("Times", 15))
        convert_text.place(relx=0.05, rely=0.8, relheight=0.04)

        self.consestancey_text = consestancey_text
        self.formating_text = formating_text
        self.convert_text = convert_text
        self.codec_text = ""

        #Graph screen 2
        next_btn = tk.Button(main_frame, text="Graph", state="disabled", font=(("Times", 15, 'bold')), padx=10, pady=5, fg="white", bg="black", command=self.go_next, activebackground='#9BBDF9')
        next_btn.place(relx=0.68, rely=0.85, relwidth=0.07, relheight=0.05)
        self.next_btn = next_btn


        #Save/Cancel
        self.txt = ""
        save = tk.Button(main_frame, text="Save", font=(("Times", 13, 'bold')), padx=10, pady=5, bg="white", fg="black", command=self.save, activebackground='#9BBDF9')
        save.place(relx=0.88, rely=0.85, relwidth=0.07, relheight=0.05)

        cancel = tk.Button(main_frame, text="Cancel", font=(("Times", 13, 'bold')), padx=10, pady=5, bg="white", fg="black", command=self.controller.destory_app,activebackground='#9BBDF9')
        cancel.place(relx=0.78, rely=0.85, relwidth=0.07, relheight=0.05)



    # get information and change the displayed text
    def get_text(self, text):
        #text is the path
        XML_object = XML(text)
        self.XML_object = XML_object
        # XML_object.validate_()
        # XML_object.format_xml()
        # XML_object.to_json()
        # XML_object.encode()
        # XML_object.decode()
        #constructor of screen2
        for label in self.code_frame.winfo_children():
            label.destroy()
        # read lines from you code
        f = open(text, 'r')
        s = f.read() #return string
        # print(s)
        if '<' in s[0]:
            self.isXml = True
        s = s.split('\n')


        # ===================================================CODE FRAME=================================================#
        # Canvas while mainFrame is code_frame given to canvas
        my_canvas = tk.Canvas(self.code_frame)
        my_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        # ScrolBar
        my_scrollbar = tk.Scrollbar(self.code_frame, orient='vertical', command=my_canvas.yview)
        my_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # horizontal
        my_scrollbar2 = tk.Scrollbar(self.code_frame, orient=tk.HORIZONTAL, command=my_canvas.xview)
        my_scrollbar2.pack(side=tk.BOTTOM, fill='x')

        my_canvas.config(xscrollcommand=my_scrollbar2.set, yscrollcommand=my_scrollbar.set)
        my_canvas.bind('<Configure>', lambda e: my_canvas.config(scrollregion=my_canvas.bbox("all")))  # bounded box for canvas

        code_second_frame = tk.Frame(my_canvas)
        my_canvas.create_window((0, 0), window=code_second_frame, anchor="nw")  # bounded box start at 0,0
        self.code_second_frame = code_second_frame

        for string in s:
            text_widget = tk.Label(self.code_second_frame, text=string, fg="black")
            text_widget.pack(side="top", anchor="nw")

        if (self.isXml):
            #destroy prevoiuse button
            self.codec_btn.destroy()
            self.codec = "Encoding"
            codec = tk.Button(self.main_frame, text=self.codec, state="disabled",font=(("Times", 15)), padx=10, pady=5, fg="white", bg="black", command= self.codec_func, activebackground='#9BBDF9')
            codec.place(relx=0.77, rely=0.6, relwidth=0.15)
            codec_text = tk.Label(self.main_frame, text=self.codec, fg="black", bg="#9BBDF9", font=("Times", 15))
            codec_text.place(relx=0.05, rely=0.85, relheight=0.04)
            self.codec_text = codec_text
            self.codec_btn = codec
        else:
            # destroy prevoiuse button
            self.codec_btn.destroy()
            self.codec = "Decoding"
            codec = tk.Button(self.main_frame, text=self.codec, state="disabled",font=(("Times", 15)), padx=10, pady=5, fg="white", bg="black", command= self.codec_func, activebackground='#9BBDF9')
            codec.place(relx=0.77, rely=0.6, relwidth=0.15)
            self.codec_btn = codec
            codec_text = tk.Label(self.main_frame, text=self.codec, fg="black", bg="#9BBDF9", font=("Times", 15))
            codec_text.place(relx=0.05, rely=0.85, relheight=0.04)
            self.codec_text = codec_text

    # send msg to Page2
    def send_msg(self, msg1, msg2):
        self.controller.pass_on_msg(msg1, msg2)

    def save(self):
        if (self.txt == ""):
            ff = open("1806171.txt", 'w')
            ff.write("You Didn''t press any button please reopen application and go with the full sequnce")
        else:
            ff = open("1806171.txt", 'w')
            ff.write(self.txt)
        self.controller.destory_app()

    def consestancy(self):
        if self.isPressed_1 != True:
            #call you function
            #elements, errors = validate(f) # error = array of tubles => (line_no, tag_name, no3_elerror)
            errors = self.XML_object.validate_()
            #meta data
            flag = True
            text = []
            for err in errors:
                if len(err) != 3:
                    text.append(f"Error at line {err[0]}")
                else:
                    text.append(f"Error at line {err[0]}, Tag Name is {err[1]}, Type of Error is {err[2]}")
            # text = ["Error at line 39", "Error at line 89"]
            self.txt = text

            for string in text:
                text_widget = tk.Label(self.result_second_frame, text=string+'\n', fg="red")
                text_widget.pack(side="top", anchor="nw")
            if flag ==True:
                if self.isXml != True:
                    self.codec_btn.destroy()
                    codec = tk.Button(self.main_frame, text=self.codec, font=(("Times", 15)), padx=10, pady=5, fg="white", bg="black", command=self.codec_func, activebackground='#9BBDF9')
                    codec.place(relx=0.77, rely=0.6, relwidth=0.15)
                else:
                    self.formating_btn.destroy()
                    formating = tk.Button(self.main_frame, text="Formating", font=(("Times", 15)), padx=10, pady=5, fg="white", bg="black", command=self.formating, activebackground='#9BBDF9')
                    formating.place(relx=0.31, rely=0.6, relwidth=0.15)
                #green
                self.consestancey_text.destroy()
                consestancey_text = tk.Label(self.main_frame, text="Consestancey", fg="green", bg="#9BBDF9", font=("Times", 15))
                consestancey_text.place(relx=0.05, rely=0.7, relheight=0.04)
            #to make data ready
            self.next_btn.destroy()
            next_btn = tk.Button(self.main_frame, text="Graph", font=(("Times", 15, 'bold')), padx=10, pady=5, fg="white", bg="black", command=self.go_next, activebackground='#9BBDF9')
            next_btn.place(relx=0.68, rely=0.85, relwidth=0.07, relheight=0.05)
            msg1, msg2 = self.XML_object.graph()
            self.send_msg(msg1, msg2)
            self.isPressed_1 = True

    def formating(self):
        if self.isPressed_2 != True:
            #call you function
            text = self.XML_object.format_xml()
            #meta data
            flag = True
            # print("435")
            # print(text)
            self.txt = text
            text = text.split('\n')
            #destroy what inside result_frame
            for widget in self.result_second_frame.winfo_children():
                widget.destroy()

            # ===================================================RESULT FRAME=========================#
            # Canvas while mainFrame is result_frame given to canvas
            my_canvasR2 = tk.Canvas(self.result_frame)
            my_canvasR2.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
            # Scrol Bar
            my_scrollbarR = tk.Scrollbar(self.result_frame, orient='vertical', command=my_canvasR2.yview)
            my_scrollbarR.pack(side=tk.RIGHT, fill=tk.Y)

            # horizontal
            my_scrollbar2R = tk.Scrollbar(self.result_frame, orient=tk.HORIZONTAL, command=my_canvasR2.xview)
            my_scrollbar2R.pack(side=tk.BOTTOM, fill=tk.X)

            my_canvasR2.config(xscrollcommand=my_scrollbar2R.set, yscrollcommand=my_scrollbarR.set)
            my_canvasR2.bind('<Configure>', lambda e: my_canvasR2.config(
                scrollregion=my_canvasR2.bbox("all")))  # bounded box for canvas

            result_second_frame = tk.Frame(my_canvasR2)
            my_canvasR2.create_window((0, 0), window=result_second_frame, anchor="nw")  # bounded box start at 0,0
            self.result_second_frame = result_second_frame

            # #print <?xml version="1.0" encoding="UTF-8"?>
            # text_widget = tk.Label(self.result_second_frame, text="""<?xml version="1.0" encoding="UTF-8"?>""", fg="black")
            # text_widget.pack(side="top", anchor="nw")

            for string in text:
                text_widget = tk.Label(self.result_second_frame, text=string, fg="black")
                text_widget.pack(side="top", anchor="nw")
            if flag ==True:
                self.convert_btn.destroy()
                convert = tk.Button(self.main_frame, text="Convert X/J", font=(("Times", 15)), padx=10, pady=5, fg="white", bg="black", command=self.convert, activebackground='#9BBDF9')
                convert.place(relx=0.54, rely=0.6, relwidth=0.15)
                #green
                self.formating_text.destroy()
                formating_text = tk.Label(self.main_frame, text="Formating", fg="green", bg="#9BBDF9", font=("Times", 15))
                formating_text.place(relx=0.05, rely=0.75, relheight=0.04)
            self.isPressed_2 = True

    def convert(self):
        if self.isPressed_3 != True:
            # call you function
            text = self.XML_object.to_json()

            # meta data
            flag = True

            self.txt = text
            text = text.split('\n')
            # destroy what inside result_frame
            for widget in self.result_second_frame.winfo_children():
                widget.destroy()

            for string in text:
                text_widget = tk.Label(self.result_second_frame, text=string, fg="black")
                text_widget.pack(side="top", anchor="nw")
            if flag == True:
                self.codec_btn.destroy()
                codec = tk.Button(self.main_frame, text=self.codec, font=(("Times", 15)), padx=10, pady=5, fg="white", bg="black", command=self.codec_func, activebackground='#9BBDF9')
                codec.place(relx=0.77, rely=0.6, relwidth=0.15)
                self.convert_text.destroy()
                convert_text = tk.Label(self.main_frame, text="Convert X/J", fg="green", bg="#9BBDF9", font=("Times", 15))
                convert_text.place(relx=0.05, rely=0.8, relheight=0.04)
            self.isPressed_3 = True

    def codec_func(self):
        if self.isPressed_4 != True:
            # call you function
            text = ""
            if self.isXml == True:
                #encode
                text = self.XML_object.encode() # XML_object.encode()
            else:
                #decode
                text = self.XML_object.decode() # XML_object.decode()

            # meta data
            flag = True
            # text = """Encoded File
            #
            # 24t8l"""
            self.txt = text
            text = text.split('\n')
            # destroy what inside result_frame
            for widget in self.result_second_frame.winfo_children():
                widget.destroy()

            for string in text:
                text_widget = tk.Label(self.result_second_frame, text=string, fg="black")
                text_widget.pack(side="top", anchor="nw")
            if flag == True:
                if self.isXml != True:
                    self.formating_btn.destroy()
                    formating = tk.Button(self.main_frame, text="Formating", font=(("Times", 15)), padx=10, pady=5, fg="white", bg="black", command=self.formating, activebackground='#9BBDF9')
                    formating.place(relx=0.31, rely=0.6, relwidth=0.15)
                self.codec_text.destroy()
                codec_text = tk.Label(self.main_frame, text=self.codec, fg="green", bg="#9BBDF9", font=("Times", 15))
                codec_text.place(relx=0.05, rely=0.85, relheight=0.04)
            self.isPressed_4 = True
    def go_next(self):
        self.send_graph()
        self.controller.show_frame(Page2)
    def send_graph(self):
        self.controller.pass_graph(True)

#screen 3
class Page2(tk.Frame):
    # flag = False
    def __init__(self, parent, controller):
        self.controller = controller
        self.flag = False
        tk.Frame.__init__(self, parent)
        #instance of Start page share same static method
        main_frame = tk.Frame(self, bg="#9BBDF9")
        main_frame.place(relwidth=1, relheight=1, relx=0, rely=0)
        self.main_frame = main_frame
        # screen 2 text
        screen2 = tk.Label(self.main_frame, text="Screen 2", fg="black", bg="#9BBDF9", font=("Times", 15))
        screen2.place(relx=0.48, rely=0.025)

        # graph it
        show_networking = tk.Button(self.main_frame, state='disabled', text="Show Graph!", font=(("Times", 15, 'bold')), padx=10, pady=5, fg="black", bg="white", command=self.graph_it, activebackground='#9BBDF9')
        show_networking.place(relx=0.4, rely=0.4, relwidth=0.2, relheight=0.2)
        self.graph_nodes = show_networking

        #Buttons
        btn_back = tk.Button(self.main_frame, text="Back", font=(("Times", 15, 'bold')), padx=10, pady=5, fg="black", bg="white", command=self.go_back, activebackground='#9BBDF9')
        btn_back.place(relx=0.78, rely=0.85, relwidth=0.07, relheight=0.05)
        cancel = tk.Button(self.main_frame, text="Close", font=(("Times", 15, 'bold')), padx=10, pady=5, bg="white", fg="black", command=self.controller.destory_app, activebackground='#9BBDF9')
        cancel.place(relx=0.88, rely=0.85, relwidth=0.07, relheight=0.05)

    def get_msg(self, msg1, msg2):
        self.adj_matrix = msg1.astype(int)
        self.marker_array = msg2
        # print(self.adj_matrix)
        # print(self.marker_array)
        self.flag = True
    def get_graph(self, flag):
        self.flag = flag
        self.graph_nodes.destroy()
        show_networking = tk.Button(self.main_frame, text="Show Graph!", font=(("Times", 15, 'bold')), padx=10, pady=5, fg="black", bg="white", command=self.graph_it, activebackground='#9BBDF9')
        show_networking.place(relx=0.4, rely=0.4, relwidth=0.2, relheight=0.2)

    def go_back(self):
        self.controller.show_frame(Page1)

    def get_edges(self):
        l = len(self.marker_array)
        edges_as_tubles = []
        for i in range(l):
            for j in range(l):
                if self.adj_matrix[i][j] == 1:
                    edges_as_tubles.append((self.marker_array[i], self.marker_array[j]))
        return edges_as_tubles
    def graph_it(self):
        if (self.flag == True):
            # directed graph
            G1 = DiGraph()
            # [(0, 1), (1, 2), (0, 4), (2, 0)]]
            edges = self.get_edges()
            G1.add_edges_from(edges)
            style.use("seaborn-dark")
            figure()
            grid()
            draw_networkx(G1, edge_color= ['blue'])
            show()

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
# app.iconbitmap(default=r"assets/xml-file.ico")
app.iconbitmap("C:/3rd Electrical Computer AI/Data Structuers and Algorithms/final________project2/xmlF/assets/xml-file.ico")

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
