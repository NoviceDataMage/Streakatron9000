from tkinter import PhotoImage, messagebox
from PIL import Image, ImageTk
import customtkinter as ctk
import json

streak_counter = 0
streak_column = 0

try:
    with open("C:/Users/Pako/Desktop/storage.json", "r") as file:
        loaded_data = json.load(file)
    streak_counter = loaded_data["counter_bath"]

except (FileNotFoundError, KeyError):
    print("No saved data found. Initializing streak_counter to 0.")
    streak_counter = 0

def save(data):
    with open("C:/Users/Pako/Desktop/storage.json", "w") as file:
        json.dump(data, file)  

def reset(name):
    global streak_counter
    streak_counter = 0

    data = {name: streak_counter}

    save(data)

    output_label.configure(text=str(streak_counter))

def message_box(name):
    result = messagebox.askyesno(
        title='Reset',
        message='Are You Sure?'
    )

    if result:
        reset(name)

    print(result)

def streak(name):
    global streak_counter, flash_timer_id
    streak_counter += 1

    data = {name: streak_counter}

    with open("C:/Users/Pako/Desktop/storage.json", "w") as file:
        json.dump(data, file)  

        output_label.configure(text=str(streak_counter))
    
    # Debouncer
    if flash_timer_id is not None:
        root.after_cancel(flash_timer_id)

    flash_timer_id = root.after(500, wisp_blink)
    
def update_image(image_path):
    global tk_image 

    new_image = Image.open(image_path)
    tk_image = ImageTk.PhotoImage(new_image)

    image_label.configure(image=tk_image)
    image_label.image = tk_image


def wisp_blink():
    root.after(500, lambda: update_image(img_wisp_blink))

    root.after(700, lambda: update_image(img_wisp_open))

    root.after(900, lambda: update_image(img_wisp_blink))

    root.after(1100, lambda: update_image(img_wisp_open))

def add_streak(streak=None):
    global streak_column

    if not streak:
        streak = streak_entry.get()
    if streak:
        streak_frame = ctk.CTkFrame(canvas, bg_color="#7d7d7d")
        streak_label = ctk.CTkLabel(streak_frame, text=f"{streak}", 
                                  bg_color="#2a3e5e", fg_color="#3c6cba")
        streak_label.pack(pady=10)

        streak_number_label = ctk.CTkLabel(streak_frame, text=f"{streak_counter}", 
                                  bg_color="#2a3e5e", fg_color="#3c6cba")
        streak_number_label.pack(pady=10)

        streak_add_button = ctk.CTkButton(streak_frame, text = 'WE CLIMB.', command = lambda: streak(f"{streak}"), font = cfont , 
                                          fg_color="black", hover_color = "gray")
        streak_add_button.pack(pady=12, padx=10)

        streak_reset_button = ctk.CTkButton(streak_frame,text = 'Reset', command = lambda: message_box(f"{streak}") , font = cfont, fg_color="#5e5e5e", text_color = "Black", hover_color = "#7d7d7d")
        streak_reset_button.pack(pady=12, padx=10)

        streak_frame.pack(side="left", padx=10)

def close_overlay(event, dim_overlay):
    dim_overlay.destroy()

def show_overlay(parent):
    dim_overlay = ctk.CTkFrame(parent, fg_color="#808080", width=parent.winfo_width(), height=parent.winfo_height())
    dim_overlay.place(relx=0.5, rely=0.5, anchor="center")
    
    overlay = ctk.CTkFrame(dim_overlay, fg_color="#1c1c1c", width=300, height=200)
    overlay.place(relx=0.5, rely=0.5, anchor="center")
    
    streak_entry = ctk.CTkEntry(overlay, width=35, bg_color='#262626', fg_color="#404040",
                                font=("Obvia", 12))
    streak_entry.pack(pady=10)
    
    add_streak_button = ctk.CTkButton(overlay, text="Add New Streak",
                                      command=add_streak, 
                                      fg_color="#5e5e5e", text_color="Black", hover_color="#7d7d7d",
                                      font=("Obvia", 12))
    add_streak_button.pack(pady=5)
    
    dim_overlay.bind("<Button-1>", lambda event: close_overlay(event, dim_overlay))
    
    return overlay

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

root=ctk.CTk()
root.title("Streakatron9000")
 
root.geometry("1000x600")

dfont = ctk.CTkFont(family="Comic Sans MS", size=24, weight="bold")
cfont = ctk.CTkFont(family="Obvia", size=15, weight="bold")

canvas = ctk.CTkCanvas(root, bg="#1c1c1c")
canvas.pack(fill=ctk.BOTH, expand=True)

scrollbar = ctk.CTkScrollbar(canvas, orientation="horizontal", command=canvas.yview)
scrollbar.pack(side=ctk.BOTTOM, fill="x")

canvas.configure(xscrollcommand=scrollbar.set)
canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

add_streak_overlay_button = ctk.CTkButton(canvas, text="+",
                                  command= lambda: show_overlay(root), 
                                  fg_color="#5e5e5e", text_color="Black", hover_color="#7d7d7d",
                                  font=(cfont, 12))
add_streak_overlay_button.pack(pady=5)

root.mainloop()