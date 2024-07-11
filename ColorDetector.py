import cv2
import numpy as np
import pandas as pd
from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image

# Global variables
clicked = False
r = g = b = xpos = ypos = 0
img = None

# Reading the CSV file with pandas and giving names to each column
index = ["color", "color_name", "hex", "R", "G", "B"]
#!!!IMPORTANT!!!
#CHANGE THIS PATH TO YOUR FILE LOCATION
csv = pd.read_csv("C:/Users/VICTUS/Documents/Color Detection/colors1.csv", names=index, header=None)

# Function to calculate minimum distance from all colors and get the most matching color
def getColorName(R, G, B):
    minimum = 10000
    for i in range(len(csv)):
        d = abs(R - int(csv.loc[i, "R"])) + abs(G - int(csv.loc[i, "G"])) + abs(B - int(csv.loc[i, "B"]))
        if d <= minimum:
            minimum = d
            cname = csv.loc[i, "color_name"]
    return cname

# Function to get x, y coordinates of mouse double click
def draw_function(event, x, y, flags, param):
    global b, g, r, xpos, ypos, clicked
    if event == cv2.EVENT_LBUTTONDBLCLK:
        clicked = True
        xpos = x
        ypos = y
        b, g, r = img[y, x]
        b = int(b)
        g = int(g)
        r = int(r)

# Function to open file dialog and load image
def open_image():
    global img
    file_path = filedialog.askopenfilename()
    if file_path:
        img = cv2.imread(file_path)
        cv2.namedWindow('image')
        cv2.setMouseCallback('image', draw_function)
        while True:
            cv2.imshow("image", img)
            if clicked:
                # Draw rectangle and display color name and RGB values
                cv2.rectangle(img, (20, 20), (750, 60), (b, g, r), -1)
                text = getColorName(r, g, b) + ' R=' + str(r) + ' G=' + str(g) + ' B=' + str(b)
                cv2.putText(img, text, (50, 50), 4, 0.8, (255, 255, 255), 2, cv2.LINE_AA)
                if r + g + b >= 600:
                    cv2.putText(img, text, (50, 50), 4, 0.8, (0, 0, 0), 2, cv2.LINE_AA)
                clicked = False
            # Break the loop when user hits 'esc' key
            if cv2.waitKey(20) & 0xFF == 27:
                break
        cv2.destroyAllWindows()

# Set up the main application window
root = Tk()
root.title("Color Detection")
root.geometry("300x150")

# Set up the open image button
btn = Button(root, text="Open Image", command=open_image)
btn.pack(pady=20)

# Start the Tkinter main loop
root.mainloop()
