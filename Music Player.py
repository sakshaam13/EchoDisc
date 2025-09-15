import os
import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog
import pygame
from PIL import Image, ImageTk

# Initialize Pygame mixer
pygame.mixer.init()

# Main app window
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

root = ctk.CTk()
root.title("Vinyl Music Player")
root.geometry("700x600")

current_song = None
paused = False
vinyl_angle = 0
rotating = False

# Load vinyl image
vinyl_img = Image.open("vinyl.png").resize((250, 250)) 
vinyl_photo = ImageTk.PhotoImage(vinyl_img)
vinyl_label = ctk.CTkLabel(root, image=vinyl_photo, text="")
vinyl_label.pack(pady=20)

song_label = ctk.CTkLabel(root, text="No song loaded", font=("Courier", 16))
song_label.pack(pady=10)

def load_song():
    global current_song
    file_path = filedialog.askopenfilename(filetypes=[("MP3 Files", "*.mp3")])
    if file_path:
        current_song = file_path
        song_label.configure(text=os.path.basename(file_path))

def play_song():
    global current_song, paused, rotating
    if current_song:
        if paused:
            pygame.mixer.music.unpause()
            paused = False
            rotating = True
            rotate_vinyl()
        else:
            pygame.mixer.music.load(current_song)
            pygame.mixer.music.play()
            rotating = True
            rotate_vinyl()

def pause_song():
    global paused, rotating
    pygame.mixer.music.pause()
    paused = True
    rotating = False

def stop_song():
    global rotating
    pygame.mixer.music.stop()
    rotating = False

def rotate_vinyl():
    global vinyl_angle, rotating
    if rotating:
        vinyl_angle += 5
        rotated = vinyl_img.rotate(vinyl_angle)
        new_photo = ImageTk.PhotoImage(rotated)
        vinyl_label.configure(image=new_photo)
        vinyl_label.image = new_photo
        root.after(100, rotate_vinyl)  # keep rotating every 100ms

# Buttons
btn_frame = ctk.CTkFrame(root)
btn_frame.pack(pady=20)

load_btn = ctk.CTkButton(btn_frame, text="📂 Load", command=load_song)
play_btn = ctk.CTkButton(btn_frame, text="▶ Play", command=play_song)
pause_btn = ctk.CTkButton(btn_frame, text="⏸ Pause", command=pause_song)
stop_btn = ctk.CTkButton(btn_frame, text="⏹ Stop", command=stop_song)

load_btn.grid(row=0, column=0, padx=10, pady=10)
play_btn.grid(row=0, column=1, padx=10, pady=10)
pause_btn.grid(row=0, column=2, padx=10, pady=10)
stop_btn.grid(row=0, column=3, padx=10, pady=10)

# Volume slider
def set_volume(val):
    pygame.mixer.music.set_volume(float(val))

volume_slider = ctk.CTkSlider(root, from_=0, to=1, number_of_steps=10, command=set_volume)
volume_slider.set(0.5)
volume_slider.pack(pady=20)

root.mainloop()
