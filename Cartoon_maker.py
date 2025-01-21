import cv2
import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
import numpy as np

# Initialize the main window
top = tk.Tk()
top.geometry('800x800')  # Adjust window size to fit all elements properly
top.title('Cartoonify Your Image!')
top.configure(background='white')

# Add labels to display the images
label_original = Label(top)
label_original.grid(row=0, column=0, padx=10, pady=10)

label_sketch = Label(top)
label_sketch.grid(row=0, column=1, padx=10, pady=10)

label_cartoon = Label(top)
label_cartoon.grid(row=1, column=0, padx=10, pady=10)

label_animated = Label(top)
label_animated.grid(row=1, column=1, padx=10, pady=10)

# Add a message label to prompt the user to press 'q' to capture
message_label = Label(top, text="Press 'q' to Capture", font=('calibri', 12, 'bold'))
message_label.grid(row=2, column=0, columnspan=2, pady=10)

def resize_image(image, width, height):
    """Resize an image to fit within a specified width and height."""
    return cv2.resize(image, (width, height))

def capture_from_webcam():
    # Start the webcam
    cap = cv2.VideoCapture(0)

    def show_frame():
        ret, frame = cap.read()
        if ret:
            # Resize the frame for display
            frame_resized = resize_image(frame, 320, 240)
            frame_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame_rgb)
            imgtk = ImageTk.PhotoImage(image=img)
            label_original.imgtk = imgtk
            label_original.configure(image=imgtk)

        label_original.after(10, show_frame)  # Call this function again to keep updating the frame

    show_frame()  # Start showing webcam frames

    def capture_image():
        ret, frame = cap.read()
        if ret:
            ImagePath = 'captured_image.jpg'
            cv2.imwrite(ImagePath, frame)
            cap.release()
            cartoonify(ImagePath)  # Call cartoonify after capturing image
        else:
            print("Failed to capture image")

    # Capture when the user presses the 'q' key
    top.bind('<q>', lambda event: capture_image())

    top.mainloop()

def cartoonify(ImagePath):
    # Read the original image
    original_image = cv2.imread(ImagePath)
    original_image_resized = resize_image(original_image, 320, 240)

    # Display the original image
    original_pil = Image.fromarray(cv2.cvtColor(original_image_resized, cv2.COLOR_BGR2RGB))
    original_tk = ImageTk.PhotoImage(original_pil)
    label_original.imgtk = original_tk
    label_original.configure(image=original_tk)

    # Convert to grayscale and apply effects
    gray_scale_image = cv2.cvtColor(original_image_resized, cv2.COLOR_BGR2GRAY)
    smooth_gray_scale = cv2.medianBlur(gray_scale_image, 5)
    sketch_image = cv2.adaptiveThreshold(smooth_gray_scale, 255, 
                                         cv2.ADAPTIVE_THRESH_MEAN_C,
                                         cv2.THRESH_BINARY, 9, 9)

    # Display the sketch image
    sketch_pil = Image.fromarray(sketch_image)
    sketch_tk = ImageTk.PhotoImage(sketch_pil)
    label_sketch.imgtk = sketch_tk
    label_sketch.configure(image=sketch_tk)

    # Apply bilateral filter for the cartoon effect
    color_image = cv2.bilateralFilter(original_image_resized, 9, 300, 300)
    get_edge = cv2.adaptiveThreshold(smooth_gray_scale, 255, 
                                     cv2.ADAPTIVE_THRESH_MEAN_C,
                                     cv2.THRESH_BINARY, 9, 9)
    cartoon_image = cv2.bitwise_and(color_image, color_image, mask=get_edge)

    # Display the cartoonified image
    cartoon_pil = Image.fromarray(cartoon_image)
    cartoon_tk = ImageTk.PhotoImage(cartoon_pil)
    label_cartoon.imgtk = cartoon_tk
    label_cartoon.configure(image=cartoon_tk)

    # Apply blur effect for an animated look
    animated_image = cv2.GaussianBlur(cartoon_image, (15, 15), 0)

    # Display the animated image
    animated_pil = Image.fromarray(animated_image)
    animated_tk = ImageTk.PhotoImage(animated_pil)
    label_animated.imgtk = animated_tk
    label_animated.configure(image=animated_tk)

    # Save the cartoonified image
    cartoon_image_path = 'cartoonified_image.jpg'
    cv2.imwrite(cartoon_image_path, cartoon_image)
    print(f"Cartoonified image saved at {cartoon_image_path}")

# Button to start webcam capture
webcam_button = Button(top, text="Capture from Webcam", command=capture_from_webcam, padx=10, pady=5)
webcam_button.configure(background='#364156', foreground='white', font=('calibri', 10, 'bold'))
webcam_button.grid(row=3, column=0, columnspan=2, pady=20)

top.mainloop()
