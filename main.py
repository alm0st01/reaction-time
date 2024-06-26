import time
import random
import threading
import pynput.keyboard as k

import tkinter as tk
from customtkinter import *

import webbrowser

app = CTk(fg_color="white")
app.geometry("495x600")
app.title("Reaction Time")
app.resizable(0,0)

running = False  # This is true anytime between the start of the countdown and the end of the stopwatch
isOn = False  # This is true anytime during the stopwatch thread
jump_check = False  # Required to stop a runtime bug
def round_rectangle(x1, y1, x2, y2, radius=25, **kwargs):
    points = [x1+radius, y1,
            x1+radius, y1,
            x2-radius, y1,
            x2-radius, y1,
            x2, y1,
            x2, y1+radius,
            x2, y1+radius,
            x2, y2-radius,
            x2, y2-radius,
            x2, y2,
            x2-radius, y2,
            x2-radius, y2,
            x1+radius, y2,
            x1+radius, y2,
            x1, y2,
            x1, y2-radius,
            x1, y2-radius,
            x1, y1+radius,
            x1, y1+radius,
            x1, y1]

    return canvas.create_polygon(points, **kwargs, smooth=True)



def color_change(col: int, arr: list, color: str):
    canvas.itemconfigure(arr[0+2*(col-1)], fill=color)
    canvas.itemconfigure(arr[1+2*(col-1)], fill=color)

def color_reset(arr: list):
    for i in range(1,6,1):
            canvas.itemconfigure(arr[0 + 2 * (i - 1)], fill="#222222")
            canvas.itemconfigure(arr[1 + 2 * (i - 1)], fill="#222222")

def jumpstart():
    global running
    global jump_check

    jump_check = True
    running = False
    txt.configure(text="JUMPSTART!")

    time.sleep(0.45)  # Used to combat against possible runtime bugs
    jump_check = False

def stopwatch():
    global isOn
    start_time = time.time()

    while isOn:
        txt.configure(text=f'{time.time()-start_time:.3f}')
        time.sleep(0.001)


def countdown():
    global jump_check
    global isOn
    global running
    running = True
    for i in range(1, 5, 1):  # There are multiple "if running and not jump_check" statements to stop for any jumpstarts
        if running:
            color_change(i, circle_r, "red")
            print(i)
            time.sleep(1)
    if running:
        color_change(5, circle_r, "red")
        print(5)
        if running:
            time.sleep(random.uniform(0.2, 3))
    if running:
        print("go!")
        color_reset(circle_r)
        jump_check = False
        isOn = True
        stopwatch_thread = threading.Thread(target=stopwatch)
        stopwatch_thread.start()


canvas = tk.Canvas(app, bg="white", height=600, width=495)
hb = []
circle_n = []
circle_r = []

for i in range(1, 6, 1):
    # appending headlight backgrounds
    hb.append(round_rectangle(20 + 95 * (i - 1), 50, 95 * i, 250, fill="black"))
    # appending circles per column
    for a in range(1, 3, 1):
        # appending 2 regular circles per column
        circle_n.append(canvas.create_oval(35+95*(i-1), 54+49*(a-1), 80+95*(i-1), 99+49*(a-1), fill="#222222", outline="black"))
    for b in range(1, 3, 1):
        # appending 2 color-changing circles per column
        circle_r.append(canvas.create_oval(35+95*(i-1), 152+49*(b-1), 80+95*(i-1), 197+49*(b-1), fill="#222222", outline="black"))

# 0,20,95,115,190,210,285,305,380,400
# 20, 115, 210, 305
# 95, 190, 285, 380

txt = CTkLabel(app, text="",text_color="black", font=("Calibria",62))
txt.place(x=247,y=300, anchor=CENTER)

instr = CTkLabel(app, text="Press the spacebar to start, and press it again when all lights are off.", text_color="black", font=("Calibria",14))
instr.place(x=247, y=25, anchor=CENTER)

canvas.pack()

gLabel = CTkLabel(app, text= "github.com/alm0st01",font=("Arial", 16,'underline'), text_color="black")
gLabel.place(x=25,y=560)
gLabel.bind("<Button-1>", lambda e: webbrowser.open_new("https://github.com/alm0st01"))

def on_press(key):
    global running
    global isOn
    global jump_check
    if str(key) == "Key.space":
        if running:
            if isOn:
                isOn = False
            else:
                jumpstart()
            running = False
        else:
            txt.configure(text="0.000")
            color_reset(circle_r)
            countdown_thread = threading.Thread(target=countdown)
            countdown_thread.start()


def listen():
    if not jump_check:
        with k.Listener(on_press=on_press) as listener:
            listener.join()


listen_thread = threading.Thread(target=listen)
listen_thread.start()

app.mainloop()