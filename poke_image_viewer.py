"""
Description:
  Graphical user interface that displays the official artwork for a
  user-specified Pokemon, which can be set as the desktop background image.

Usage:
  python poke_image_viewer.py
"""
from tkinter import *
from tkinter import ttk
import tkinter as tk
import os
from image_lib import *
from poke_api import *
from PIL import Image, ImageTk

from poke_api import get_pokemon_names # type: ignore


# Get the script and images directory
script_dir = os.path.dirname(os.path.abspath(__file__))
images_dir = os.path.join(script_dir, 'images')

# TODO: Create the images directory if it does not exist
if not os.path.exists(images_dir):
  os.makedirs(images_dir)

class PokemonGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Pokemon Artwork Viewer")
        self.root.iconbitmap('pokemon.ico')  # Replace 'pokemon_icon.ico' with your icon file

        self.selected_pokemon = tk.StringVar()
        self.image_path = tk.StringVar()
        self.image_path.set('pokemon.jpg') 
        self.image_label = None
        
        self.desktop_image_button = None

        self.create_gui()
        self.update_image(None)

    def create_gui(self):
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0)

        ttk.Label(main_frame, text="Select a Pokemon:").grid(row=1, column=0, padx=5, pady=5)
        pokemon_combobox = ttk.Combobox(main_frame, textvariable=self.selected_pokemon, width=30, state="readonly")
        pokemon_combobox.grid(row=1, column=1, padx=5, pady=5)
        pokemon_combobox.bind("<<ComboboxSelected>>", self.update_image)

        self.image_label = ttk.Label(main_frame)
        self.image_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

        self.desktop_image_button = ttk.Button(main_frame, text="Set as Desktop Image", state="disabled", command=self.set_desktop_image)
        self.desktop_image_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        # Populate combobox with Pokemon names
        pokemon_names = get_pokemon_names()
        pokemon_combobox['values'] = pokemon_names

    def update_image(self, event):
        pokemon_name = self.selected_pokemon.get()
        if pokemon_name:
            image_path = download_pokemon_artwork(pokemon_name)
            
            self.image_path.set(image_path)
            img = Image.open(image_path)
            img = img.resize(scale_image(img.size), Image.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            self.image_label.config(image=photo)
            self.image_label.image = photo
            self.desktop_image_button.config(state="normal")
        else:
            # put deault image
            img = Image.open('pokemon.jpg')
            img = img.resize(scale_image(img.size), Image.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            self.image_label.config(image=photo)
            self.image_label.image = photo          
            self.desktop_image_button.config(state="disabled")
            
            
    def set_desktop_image(self):
        image_path = os.path.abspath(self.image_path.get())
        set_desktop_background_image(image_path)

    
if __name__ == "__main__":
    root = tk.Tk()
    app = PokemonGUI(root)
    root.mainloop()