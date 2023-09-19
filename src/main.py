import cv2
from pyzbar.pyzbar import decode
import numpy as np
import os
import tkinter as tk
import PIL.Image, PIL.ImageTk
from tkinter import messagebox, filedialog
import pyperclip



def main():
    global data_lbl, canvas, root
    root = tk.Tk()


    window_width = 700
    window_hight = 600
        
    monitor_width = root.winfo_screenwidth()
    monitor_hight = root.winfo_screenheight()
        
    x = (monitor_width / 2) - (window_width / 2)
    y = (monitor_hight / 2) - (window_hight / 2)

    root.geometry(f'{window_width}x{window_hight}+{int(x)}+{int(y)}')
    root.title("JK QR Code Reader")
    #root.iconbitmap("JK.ico")
    root.config(bg="#dbdbdb")


    canvas = tk.Canvas(root, width=1280, height=720, bg="black")
    canvas.pack(pady=15)

    data_lbl = tk.Label(root, text="", font=("Arial", 14), bg="#dbdbdb")
    data_lbl.pack(pady=10)

    read_btn = tk.Button(root, font=("Arial", 14), width=20, text="Read QR code", command=get_qrcode)
    read_btn.pack(pady=10)

    copy_btn = tk.Button(root, font=("Arial", 14), width=20, text="Copy", command=copy)
    copy_btn.pack(pady=10)

    


    root.mainloop()



def copy():
    data = data_lbl["text"]

    if data and data != "No QR codes found in image!":
        pyperclip.copy(data)
        messagebox.showinfo("Info", "Succesfully copied to clipboard...")
        return
    
    messagebox.showerror("Error", "Nothing to copy!")



def get_qrcode():
    path = filedialog.askopenfilename(title="Open", defaultextension=".png", filetypes=[("PNG Files", "*.png"), ("JPEG Files", "*.jpg"), ("JPEG Files", "*.jpeg"), ("All Files", "*.*")])

    if not path:
        return


    try:
        data, image = read(path)
    except:
        messagebox.showerror("Error", "Invalid image file!")
        return
    

    formated_data = []
    for i in data:
        formated_data.append(f"{i[0]:10}: {i[1]}")

    data_lbl["text"] = "\n".join(formated_data) if len("\n".join(formated_data)) != 0 else "No QR codes found in image!"

    canvas.create_image(0, 0, anchor=tk.NW, image=image)



def read(path, max_width=1280, max_height=720):
    if not os.path.isfile(path):
        print(False)
        return False # return (None, None)


    image = cv2.imread(path)

    original_height, original_width, _ = image.shape
    scale_factor = min(max_width / original_width, max_height / original_height)
    resized_image = cv2.resize(image, None, fx=scale_factor, fy=scale_factor)

    decoded_obj = decode(resized_image)

    content = []

    for obj in decoded_obj:
        data = obj.data.decode()
        obj_type = obj.type

        content.append((obj_type, data))

        #print(f"Type: {obj_type}\nData: {data}")

        points = obj.polygon
        if len(points) > 4:
            hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
            points = hull
            
        for i in range(4):
            cv2.line(resized_image, tuple(points[i]), tuple(points[(i + 1) % 4]), (0, 0, 255), 3)


    display_image = PIL.Image.fromarray(cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB))
    #display_image.save("img.png")
    photo_image = PIL.ImageTk.PhotoImage(display_image)

        
    return (content, photo_image)



if __name__ == "__main__":
    main()

