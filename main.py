try:
    import os
except ImportError:
    print("os module not found")
    input("Press Enter to continue...")
try:
    import pyautogui
except ImportError:
    print("pyautogui module not found")
    input("Press Enter to continue...")
try:
    from PIL import Image
except ImportError:
    print("PIL module not found")
    input("Press Enter to continue...")
try:
    import tkinter as tk
    from tkinter import filedialog as fd
except ImportError:
    print("tkinter module not found")
    input("Press Enter to continue...")
#координаты заданы для разрешения 1920x1080 если у вас другое разрешение зайдите в файл cord.py через блокнот и измените их
try:
    import cord
    print("Load successfully!")
except ImportError:
    print("Cord file (cord.py) not found")
    input("Press Enter to continue...")
#coordinates are set for 1920x1080 resolution, if you have a different resolution, go to the cord.py file using notepad and change them

print("please use ONLY .png image")
print("пожалуйста используйте только .png изображение")
image_path = fd.askopenfilename()
if not os.path.exists(image_path):
    raise FileNotFoundError("image not found")
print(image_path)
    
image = Image.open(image_path)
pixels = list(image.getdata())
width, height = image.size

def on_drag(event):
    root.geometry(f"+{event.x_root}+{event.y_root}")

def change_color(r, g, b):
    pyautogui.click(cord.colorpicker_x, cord.colorpicker_y)
    pyautogui.click(cord.colorpickerR_x, cord.colorpickerR_y)
    pyautogui.typewrite(str(r))
    pyautogui.click(cord.colorpickerG_x, cord.colorpickerG_y)
    pyautogui.typewrite(str(g))
    pyautogui.click(cord.colorpickerB_x, cord.colorpickerB_y)
    pyautogui.typewrite(str(b))

def draw_image_by_colors(pixels,start_x,start_y):
    color_positions = {}

    for y in range(height):
        for x in range(width):
            r, g, b = pixels[y * width + x][:3]

            if (r, g, b) == (255, 255, 255):
                continue

            if (r, g, b) not in color_positions:
                color_positions[(r, g, b)] = []
            color_positions[(r, g, b)].append((x, y))

    for color, positions in color_positions.items():
        change_color(*color)

        while positions:
            x1, y1 = positions.pop(0)
            pyautogui.moveTo(start_x + x1, start_y + y1)

            line_positions = [(x1, y1)]
            while positions and positions[0][1] == y1 and positions[0][0] == x1 + 1:
                x1, y1 = positions.pop(0)
                line_positions.append((x1, y1))

            if len(line_positions) > 1:
                x_start, y_start = line_positions[0]
                x_end, y_end = line_positions[-1]
                pyautogui.mouseDown(start_x + x_start, start_y + y_start)
                pyautogui.moveTo(start_x + x_end, start_y + y_end, duration=0.1)
                pyautogui.mouseUp()
            else:
                pyautogui.click(start_x + x1, start_y + y1)

def on_close():
    global start_x, start_y
    start_x = canvas.winfo_rootx()
    start_y = canvas.winfo_rooty()
    root.destroy()
    
root = tk.Tk()
root.title("Close to start!")
canvas = tk.Canvas(root, width=width, height=height)
canvas.pack()
img = tk.PhotoImage(file=image_path)
canvas.create_image(0, 0, anchor=tk.NW, image=img)
root.bind('<B1-Motion>', on_drag)
root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()
draw_image_by_colors(pixels,start_x,start_y)
