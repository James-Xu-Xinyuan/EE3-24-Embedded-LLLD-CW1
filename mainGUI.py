from PIL import Image, ImageTk
###########################

import paho.mqtt.client as mqtt
client = mqtt.Client()

import json
import math

##########################

import matplotlib
matplotlib.use("TkAgg")

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure

import matplotlib.animation as animation
from matplotlib import style

import tkinter as tk
from tkinter import ttk

import random
import time


LARGE_FONT = ("Verdana",12)
XLARGE_FONT = ("Verdana",32)
style.use("ggplot")

f = Figure(figsize=(2,6), dpi=100)
a = f.add_subplot(111)

xList = list(range(1,21))
yList = [0] * 20
temp_list = [0]*2


average_counter = 1
current_average = 0
current_maximun = 0
def animate(i):
    
    #print(yList)
    calculate_average(yList[19])
    '''
    print("yList[19]: ",yList[19])
    print("average_counter: ",average_counter)
    print("current_average: ", current_average)
'''
    calculate_maximun(yList[19])
    #print("current_maximun: ", current_maximun)
    
    a.clear()
    a.plot(xList,yList,'#EF5893')
    title = "Current Maximun: "+str(int(current_maximun))+"\nCurrent Average: "+str(int(current_average))
    a.set_title(title)

###################################

def calculate_average(new_input): #this function calculate the avaerage acceleration
    global average_counter
    global current_average
    current_average = (average_counter-1)/average_counter*current_average + new_input/average_counter
    average_counter += 1

def calculate_maximun(new_input):#this function keep the max acceleration
    global current_maximun
    if(current_maximun < abs(new_input)):
        current_maximun = new_input
    

def on_message(client, userdata, message) :#handle the raw data and scalarize it
    #convert raw data to readable data
    one_reading = message.payload
    raw_data = one_reading.decode('utf8').replace("'", '"')
    json_acceptable_string = raw_data.replace("'", "\"")
    d = json.loads(json_acceptable_string)
    one_d_output = int(math.sqrt((d['x'])**2+(d['y'])**2+(d['z'])**2))
    del temp_list[0]
    temp_list.append(one_d_output)
    del yList[0] #delete last item in the list
    yList.append(abs(temp_list[1]-temp_list[0]))
    
    
    


client.on_message = on_message
client.connect("broker.mqttdashboard.com",port=1883)
client.subscribe("IC.embedded/LLLD/#")
client.loop_start()
###################################
    

class LLLDapp(tk.Tk):#main app

    def __init__(self,*args,**kwargs):
        #client.loop_start()

        
        tk.Tk.__init__(self,*args,**kwargs)

        
        tk.Tk.wm_title(self,"LLLD")

        
        container = tk.Frame(self)
        container.pack(side="top",fill="both",expand=True)

        container.grid_rowconfigure(0,weight=1)
        container.grid_columnconfigure(0,weight=1)

        self.frames = {}

        for F in (StartPage,PageOne,PageTwo,PageThree):            
            frame = F(container,self)
            self.frames[F] = frame
            
            frame.grid(row=0, column=0, sticky="nsew")
            

        self.show_frame(StartPage)

    def show_frame(self,cont):

        frame = self.frames[cont]
        frame.tkraise()


    


class StartPage(tk.Frame):

    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)

        label_img = Image.open("Welcome_page.jpg")
        label_img =label_img.resize((400, 600), Image.ANTIALIAS)
        label = tk.Label(self,text="Welcome to LLLD", font=XLARGE_FONT)
        label.img = ImageTk.PhotoImage(label_img)
        label['image'] = label.img
        label.pack()

        
        img = Image.open("llld_logo.jpg")
        img = img.resize((80, 30), Image.ANTIALIAS)
        button1 = tk.Button(self, #text="Page One",
                            command=lambda: controller.show_frame(StartPage))
        button1.img = ImageTk.PhotoImage(img)
        button1.config(height = 30, width = 80)
        button1['image'] = button1.img
        button1.grid(row = 1,column = 1)
        button1.pack(side = "left", anchor= 's')

        img2 = Image.open("now_playing.jpg")
        img2 = img2.resize((80, 30), Image.ANTIALIAS)
        button2 = tk.Button(self,#text="Now Playing",
                            command=lambda: controller.show_frame(PageTwo))
        button2.img = ImageTk.PhotoImage(img2)
        button2.config(height = 30, width = 80)
        button2['image'] = button2.img
        button2.grid(row = 2,column = 1)
        button2.pack(side = "left", anchor= 's')


        img3 = Image.open("your_ranking.jpg")
        img3 = img3.resize((80, 30), Image.ANTIALIAS)
        button3 = tk.Button(self,#text="Connect",
                            command=lambda: controller.show_frame(PageThree))
        button3.img = ImageTk.PhotoImage(img3)
        button3.config(height = 30, width = 80)
        button3['image'] = button3.img
        button3.grid(row = 1,column = 2)
        button3.pack(side = "left", anchor= 's')

        img4 = Image.open("about_us.jpg")
        img4 = img4.resize((80, 30), Image.ANTIALIAS)
        button4 = tk.Button(self,#text="Connect",
                            command=lambda: controller.show_frame(PageOne))
        button4.img = ImageTk.PhotoImage(img4)
        button4.config(height = 30, width = 80)
        button4['image'] = button4.img
        button4.grid(row = 1,column = 2)
        button4.pack(side = "left", anchor= 's')



class PageOne(tk.Frame):#welcome page
    
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        
        about_us = "We are a group of enthusiastic uni engineering \nstudentsinterested in IoT products.\n We hope we can use the amazing technology \nto make our life better, while protecting\n our users, especially privacy. Although the\n demand of young people nowadays is highly diversified and\n innovative, we are not afraid of \nthe challenge. Our goal is to develop interesting\n products and sell them with our\n excellent service."
        label = tk.Label(self,compound = tk.CENTER,text=about_us, font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        
        img = Image.open("llld_logo.jpg")
        img = img.resize((80, 30), Image.ANTIALIAS)
        button1 = tk.Button(self, #text="Page One",
                            command=lambda: controller.show_frame(StartPage))
        button1.img = ImageTk.PhotoImage(img)
        button1.config(height = 30, width = 80)
        button1['image'] = button1.img
        button1.grid(row = 1,column = 1)
        button1.pack(side = "left", anchor= 's')

        img2 = Image.open("now_playing.jpg")
        img2 = img2.resize((80, 30), Image.ANTIALIAS)
        button2 = tk.Button(self,#text="Now Playing",
                            command=lambda: controller.show_frame(PageTwo))
        button2.img = ImageTk.PhotoImage(img2)
        button2.config(height = 30, width = 80)
        button2['image'] = button2.img
        button2.grid(row = 2,column = 1)
        button2.pack(side = "left", anchor= 's')


        img3 = Image.open("your_ranking.jpg")
        img3 = img3.resize((80, 30), Image.ANTIALIAS)
        button3 = tk.Button(self,#text="Connect",
                            command=lambda: controller.show_frame(PageThree))
        button3.img = ImageTk.PhotoImage(img3)
        button3.config(height = 30, width = 80)
        button3['image'] = button3.img
        button3.grid(row = 1,column = 2)
        button3.pack(side = "left", anchor= 's')

        img4 = Image.open("about_us.jpg")
        img4 = img4.resize((80, 30), Image.ANTIALIAS)
        button4 = tk.Button(self,#text="Connect",
                            command=lambda: controller.show_frame(PageOne))
        button4.img = ImageTk.PhotoImage(img4)
        button4.config(height = 30, width = 80)
        button4['image'] = button4.img
        button4.grid(row = 1,column = 2)
        button4.pack(side = "left", anchor= 's')



class PageTwo(tk.Frame):#about me page
    
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        label = ttk.Label(self,text="Page Two", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        
        button1 = ttk.Button(self,text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = ttk.Button(self,text="Page One",
                            command=lambda: controller.show_frame(PageOne))
        button2.pack()

class PageThree(tk.Frame):#graph page
    
    def __init__(self,parent,controller):
        
        tk.Frame.__init__(self,parent)
        #label = ttk.Label(self,text="Graph Page", font=LARGE_FONT)
        #label.pack(pady=10,padx=10)

        img = Image.open("home.jpg")
        img = img.resize((80, 30), Image.ANTIALIAS)
        button1 = tk.Button(self, #text="Page One",
                            command=lambda: controller.show_frame(StartPage))
        button1.img = ImageTk.PhotoImage(img)
        button1.config(height = 30, width = 80)
        button1['image'] = button1.img
        button1.grid(row = 1,column = 1)
        button1.pack()

        canvas = FigureCanvasTkAgg(f,self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP,fill=tk.BOTH,expand=True)
        

        
        


app = LLLDapp()
ani =animation.FuncAnimation(f,animate,interval=200)
app.mainloop()
        
