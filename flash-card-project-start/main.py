from tkinter import *
import pandas as pd
import random
word = ''
BACKGROUND_COLOR = "#B1DDC6"
'# data frame'

try:
    df = pd.read_csv("data/words_to_learn.csv")
    if len(df) > 0:
        list_dict = df.to_dict(orient="records")
    else:
        df = pd.read_csv("data/french_words.csv")
        list_dict = df.to_dict(orient="records")
except FileNotFoundError:
    df = pd.read_csv("data/french_words.csv")
    list_dict = df.to_dict(orient="records")


'# function'


def word_change():
    global timer, word
    window.after_cancel(timer)
    word = random.choice(list_dict)
    canvas.itemconfig(word_french, text=word["French"])
    canvas.itemconfig(title, text="French", fill="black")
    canvas.itemconfig(canvas_image, image=front_image)
    canvas.itemconfig(word_french, text=word["French"], fill="black")
    timer = window.after(3000, func=image_change)


def image_change():
    global word
    canvas.itemconfig(canvas_image, image=back_image)
    canvas.itemconfig(title, text="English", fill="white")
    canvas.itemconfig(word_french, text=word["English"], fill="white")


def image_unknown():
    global word
    word_change()


def image_known():
    global word
    try:
        list_dict.remove(word)
    except ValueError:
        canvas.itemconfig(canvas_image, image=front_image)
        canvas.itemconfig(title, text="CONGRATULATIONS", fill="black")
        canvas.itemconfig(word_french, text="NO PENDING WORDS", fill="black", font=("Ariel", 30, "italic"))
    try:
        word_change()
    except IndexError:
        print("No more words on the list")


window = Tk()
window.title("Flash Card Project")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
rand_word = 0

timer = window.after(3000, func=image_change)

'# canvas create'


canvas = Canvas(width=800, height=526)
front_image = PhotoImage(file="images/card_front.png")
back_image = PhotoImage(file="images/card_back.png")
canvas_image = canvas.create_image(400, 263, image=front_image)
canvas.grid(column=0, row=0, columnspan=2)
title = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
word_french = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))

'# button right'


right = PhotoImage(file="images/right.png")
button_right = Button(image=right, highlightthickness=0, command=image_known)
button_right.grid(column=1, row=1)

# button wrong
wrong = PhotoImage(file="images/wrong.png")
button_wrong = Button(image=wrong, highlightthickness=0, command=image_unknown)
button_wrong.grid(column=0, row=1)

word_change()

window.mainloop()

df_end = pd.DataFrame(list_dict)
df_end.to_csv('data/words_to_learn.csv', index= False)
