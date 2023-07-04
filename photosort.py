import os
import shutil
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox
from tkinter import filedialog

desired_height = 1200

class PhotoApp:
    def __init__(self, root):
        self.root = root
        self.photo_dir = None
        self.photo = []

        self.index = 0

        self.canvas = tk.Canvas(root)
        self.canvas.pack(fill='both', expand=True)

        self.root.bind('<Left>', self.prev_photo)
        self.root.bind('<Right>', self.next_photo)
        self.root.bind('x', self.move_to_trash)
        self.root.bind('y', self.keep_photo)
        self.root.bind('+', self.view_larger)
        self.root.bind('-', self.view_smaller)

        self.photo_dir = filedialog.askdirectory()

        if self.photo_dir:
            self.photo_files = sorted([f for f in os.listdir(self.photo_dir) if f.endswith(('.png', '.jpg', '.jpeg', '.heic', '.arw', '.raw', '.gif', '.webp', '.PNG', '.JPG', '.JPEG', '.HEIC', '.ARW', '.RAW', '.GIF', '.WEBP'))])
            if not self.photo_files:
                messagebox.showerror("Error", "No .jpg files found in directory")
                return
            self.show_photo()

    def show_photo(self):
        self.photo_image = Image.open(os.path.join(self.photo_dir, self.photo_files[self.index]))
        
        # Rotate the photo based on its EXIF orientation
        self.photo_image = self.rotate_image(self.photo_image)
        width, height = self.photo_image.size
        new_width = int(desired_height * width / height)
        self.photo_image = self.photo_image.resize((new_width, desired_height), Image.ANTIALIAS)

        # self.photo_image = self.photo_image.resize((1600, int(1600 * self.photo_image.height / self.photo_image.width)), Image.ANTIALIAS)
        self.tk_image = ImageTk.PhotoImage(self.photo_image)
        self.canvas.create_image(0, 0, anchor='nw', image=self.tk_image)


    def rotate_image(self, image):
        try:
            exif = image.getexif()
            if exif is not None:
                orientation = exif.get(0x0112)
                if orientation == 3:
                    return image.rotate(180, expand=True)
                elif orientation == 6:
                    return image.rotate(270, expand=True)
                elif orientation == 8:
                    return image.rotate(90, expand=True)
        except Exception as e:
            print("Error rotating image:", str(e))
        return image



    def next_photo(self, event):
        self.index = (self.index + 1) % len(self.photo_files)
        self.show_photo()

    def prev_photo(self, event):
        self.index = (self.index - 1) % len(self.photo_files)
        self.show_photo()

    def move_to_trash(self, event):
        shutil.move(os.path.join(self.photo_dir, self.photo_files[self.index]), os.path.join(self.photo_dir, 'trash'))
        self.photo_files.pop(self.index)
        self.index = min(self.index, len(self.photo_files) - 1)
        self.show_photo()

    def keep_photo(self, event):
        shutil.move(os.path.join(self.photo_dir, self.photo_files[self.index]), os.path.join(self.photo_dir, 'keep'))
        self.photo_files.pop(self.index)
        self.index = min(self.index, len(self.photo_files) - 1)
        self.show_photo()

    def view_larger(self, event):
        global desired_height
        desired_height = desired_height + 50
        self.show_photo()
    
    def view_smaller(self, event):
        global desired_height
        desired_height = desired_height - 50
        self.show_photo()

if __name__ == '__main__':
    root = tk.Tk()
    root.title("PhotoSort")
    root.geometry('1600x1600')
    app = PhotoApp(root)
    root.mainloop()
