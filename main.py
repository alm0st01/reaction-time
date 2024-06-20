import time
import random
import threading
import pynput.keyboard as k

import tkinter as tk
from customtkinter import *

app = CTk(fg_color="white")
app.geometry("495x600")
app.title("Reaction Time")

running = False
timer_on = False

isOn = False

stopwatch_amt = 0
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
    running = False
    txt.configure(text="JUMPSTART!")


def stopwatch():
    global stopwatch_amt
    global isOn
    stopwatch_amt = 0
    start_time = time.time()
    while isOn:
        txt.configure(text=f'{time.time()-start_time:.3f}')
        time.sleep(0.001)

    #while isOn:
    #    stopwatch_amt += 0.01
    #    #txt.configure(text='{0:.2g}'.format(stopwatch_amt))
    #    txt.configure(text=f'{stopwatch_amt:.2f}')
    #    time.sleep(0.01)


def countdown():
    global isOn
    global running
    global timer_on
    running = True
    for i in range(1, 5, 1):
        # print(i)
        if running:
            color_change(i, circle_r, "red")
            print(i)
            time.sleep(1)
        else:
            return
    if running:
        color_change(5, circle_r, "red")
        if running:
            time.sleep(random.uniform(0.2, 3))
    if running:
        print("go!")
        color_reset(circle_r)
        timer_on = True
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
        # appending 2 changing circles per column
        circle_r.append(canvas.create_oval(35+95*(i-1), 152+49*(b-1), 80+95*(i-1), 197+49*(b-1), fill="#222222", outline="black"))

# 0,20,95,115,190,210,285,305,380,400
# 20, 115, 210, 305
# 95, 190, 285, 380

txt = CTkLabel(app, text="",text_color="black", font=("Calibria",62))

txt.place(x=247,y=300, anchor=CENTER)
canvas.pack()


def on_press(key):
    global running
    global timer_on
    global isOn

    if str(key) == "Key.space":
        if running:
            if isOn:
                isOn = False
            else:
                jumpstart()
            running = False
        else:
            txt.configure(text="0.000")
            timer_on = False
            color_reset(circle_r)
            countdown_thread = threading.Thread(target=countdown)
            countdown_thread.start()


def listen():
    with k.Listener(on_press=on_press) as listener:
        listener.join()


listen_thread = threading.Thread(target=listen)
listen_thread.start()

app.mainloop()