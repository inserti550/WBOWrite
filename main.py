import time
import os
import threading
from tkinter import *
from WBO.Tools import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tkinter import filedialog as fd
from PIL import Image, ImageTk

# Globals
global link
file = ""
img_label = None
stop_drawing = False
pause_drawing = False

def filepicker():
    global img_label, file

    file = fd.askopenfilename()
    TF.delete(1.0, END)
    TF.insert(1.0, file)

    if file:
        img = Image.open(file)
        img = img.resize((300, 300))
        img_tk = ImageTk.PhotoImage(img)

        if img_label is None:
            img_label = Label(root, image=img_tk)
            img_label.image = img_tk
            img_label.place(x=550, y=100)
        else:
            img_label.config(image=img_tk)
            img_label.image = img_tk

def apply_values():
    global link, cursor_size, start_x, start_y
    link = T.get(1.0, END).strip()
    cursor_size = int(CursorSizeEntry.get(1.0, END).strip())
    start_x = int(TX.get(1.0, END).strip())
    start_y = int(TY.get(1.0, END).strip())

def run_wbo_writer():
    def wbo_writer_task():
        global stop_drawing, pause_drawing

        apply_values()

        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        driver = webdriver.Chrome(options=chrome_options)
        os.system("CLS")

        driver.get(link)

        try:
            WebDriverWait(driver, 30).until(
                EC.invisibility_of_element((By.ID, "loadingMessage"))
            )
            print("Load successful")
            SelectPencil(driver)
            SetCursorSize(driver, int(cursor_size))

            if file:
                img = Image.open(file).convert('RGB')
                width, height = img.size
                pixels = img.load()

                color_pixels = {}
                for y in range(height):
                    for x in range(width):
                        r, g, b = pixels[x, y]
                        if (r, g, b) != (255, 255, 255):
                            color = RGBToHex(r, g, b)
                            if color not in color_pixels:
                                color_pixels[color] = []
                            color_pixels[color].append((x, y))

                for color, coordinates in color_pixels.items():
                    SetColor(driver, color)
                    current_x, current_y = start_x, start_y
                    for x, y in coordinates:
                        if stop_drawing:
                            break
                        while pause_drawing:
                            time.sleep(0.1)

                        line_start = x
                        line_end = x
                        while line_end < width - 1:
                            next_r, next_g, next_b = pixels[line_end + 1, y]
                            next_color = RGBToHex(next_r, next_g, next_b)
                            if next_color == color:
                                line_end += 1
                            else:
                                break

                        Write(driver, start_x + line_start, start_y + y, start_x + line_end, start_y + y, 0.01)

                        x = line_end + 1

                        progress = (((y) * width + (x) + 1) / (width * height)) * 100
                        progress_var.set(f"Progress: {progress:.2f}%")
                        root.update_idletasks()

        except Exception as e:
            print(f"Error: {e}")
        finally:
            driver.quit()
            progress_var.set("Completed")

    threading.Thread(target=wbo_writer_task, daemon=True).start()

def pause_wbo_writer():
    global pause_drawing
    pause_drawing = not pause_drawing
    pause_button.config(text="Resume" if pause_drawing else "Pause")

def stop_wbo_writer():
    global stop_drawing
    stop_drawing = True
    progress_var.set("Stopped")

#main

root = Tk()
root.title("WBOWriter V2")
root.geometry("900x500")
root.resizable(False, False)

start_button = Button(root, height=2, width=15, text="Start WBOWriter", command=run_wbo_writer)
apply_button = Button(root, height=2, width=15, text="Apply", command=apply_values)
pause_button = Button(root, height=2, width=15, text="Pause", command=pause_wbo_writer)
stop_button = Button(root, height=2, width=15, text="Stop", command=stop_wbo_writer)
T = Text(root, height=1, width=50)
TF = Text(root, height=1, width=15)
FilePickbutton = Button(root, height=1, width=15, text="Pick file", command=filepicker)
TX = Text(root, height=1, width=15)
TY = Text(root, height=1, width=15)
LX = Label(text="Cord X")
LY = Label(text="Cord Y")
LL = Label(text="Link")
CursorSizeLabel = Label(text="Cursor Size")
CursorSizeEntry = Text(root, height=1, width=15)

progress_var = StringVar()
progress_var.set("Progress: 0%")
progress_label = Label(root, textvariable=progress_var)

start_button.place(x=760, y=450)
apply_button.place(x=630, y=450)
pause_button.place(x=520, y=450)
stop_button.place(x=410, y=450)
T.place(x=5, y=25)
LL.place(x=5, y=3)
FilePickbutton.place(x=430, y=20)
TF.place(x=550, y=22)
TX.insert(1.0, "0")
TY.insert(1.0, "0")
TX.place(x=5, y=50)
LX.place(x=135, y=50)
TY.place(x=5, y=80)
LY.place(x=135, y=80)
CursorSizeLabel.place(x=5, y=110)
CursorSizeEntry.place(x=135, y=110)
progress_label.place(x=5, y=150)

root.mainloop()
