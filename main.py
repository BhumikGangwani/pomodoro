from tkinter import *
from winsound import *

# ---------------------------- CONSTANTS ------------------------------- #
RED = "#E84545"
ORANGE = "#FFAB76"
BLUE = "#D6E5FA"
GREEN = "#BAFFB4"
YELLOW = "#FFFDA2"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps, skipped_reps = 1, 0
break_rep = False
timer = None
timer_in_progress = "off"
count = 0


# ---------------------------- TIMER RESET ------------------------------- #
def reset_button_clicked():
    start_stop_button.config(text="Start")
    PlaySound("button_click.wav", SND_FILENAME)
    reset_timer()


def reset_timer():
    global reps, skipped_reps, timer_in_progress
    timer_in_progress = "off"
    reps = 1
    skipped_reps = 0
    window.after_cancel(timer)
    canvas.itemconfig(timer_text, text="00:00")
    timer_label.config(text="Timer", fg=GREEN)
    checkmark_label.config(text="")


# ---------------------------- TIMER MECHANISM ------------------------------- #
def start_stop_button_clicked():
    global timer_in_progress
    PlaySound("button_click.wav", SND_FILENAME)
    if timer_in_progress == "off":
        timer_in_progress = "on"
        start_stop_button.config(text="Stop")
        start_timer()
    elif timer_in_progress == "on":
        timer_in_progress = "pause"
        start_stop_button.config(text="Start")
        window.after_cancel(timer)
    else:
        timer_in_progress = "on"
        countdown()


def start_timer():
    global reps, break_rep, count
    work_seconds = WORK_MIN * 60
    short_break_seconds = SHORT_BREAK_MIN * 60
    long_break_seconds = LONG_BREAK_MIN * 60
    if reps % 8 == 0:
        count = long_break_seconds
        break_rep = True
        timer_label.config(text="Long Break", fg=GREEN)
    elif reps % 2 == 0:
        count = short_break_seconds
        break_rep = True
        timer_label.config(text="Short Break", fg=GREEN)
    else:
        count = work_seconds
        break_rep = False
        timer_label.config(text="Work", fg=RED)
    reps += 1
    countdown()


# --------------------------- COUNTDOWN MECHANISM ------------------------------- #
def countdown():
    global timer, count, reps, skipped_reps
    minutes_remaining = count // 60
    seconds_remaining = count % 60
    if seconds_remaining < 10:
        seconds_remaining = f"0{seconds_remaining}"
    canvas.itemconfig(timer_text, text=f"{minutes_remaining}:{seconds_remaining}")
    if count > 0:
        count -= 1
        timer = window.after(1000, countdown)
    else:
        PlaySound("alarm.wav", SND_FILENAME)
        start_timer()
        marks = ""
        for _ in range((reps - skipped_reps) // 2):
            marks += "✔"
        if break_rep:
            checkmark_label.config(text=marks)


# ---------------------------- SKIP MECHANISM ------------------------------- #
def skip_button_clicked():
    global skipped_reps
    PlaySound("button_click.wav", SND_FILENAME)
    skipped_reps += 1
    window.after_cancel(timer)
    start_timer()


# ---------------------------- UI SETUP ------------------------------- #

# Window
window = Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=ORANGE)

# Canvas
canvas = Canvas(width=200, height=224, bg=ORANGE, highlightthickness=0)
tomato_img = PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(100, 130, text="00:00", fill=BLUE, font=(FONT_NAME, 35, "bold"))
canvas.grid(column=1, row=1)

# Labels
timer_label = Label(text="Timer", bg=ORANGE, fg=GREEN, font=("Arial", 45, "bold"))
timer_label.grid(column=1, row=0)

checkmark_label = Label(bg=ORANGE, fg=BLUE)
checkmark_label.grid(column=1, row=3)

# Buttons
start_stop_button = Button(text="Start", bg=YELLOW, font=("Calibri", 12), command=start_stop_button_clicked)
start_stop_button.grid(column=0, row=2)

skip_button = Button(text=">", bg=YELLOW, font=8, command=skip_button_clicked)
skip_button.place(x=58, y=295)

reset_button = Button(text="Reset", bg=YELLOW, font=("Calibri", 12), command=reset_button_clicked)
reset_button.grid(column=2, row=2)

window.mainloop()
