import tkinter as tk
#tkinder is a python library for creating GUI
from tkinter import filedialog, messagebox
#filedialog is a module for file selection dialogue
#messagebox is used for pop up messages
from PIL import Image, ImageTk
#Pillow(PIL) is a library for handling and displaying images
import cv2
#cv2 is a library for image processing task
import numpy as np
#numpy is used to perform numerical calculations and creating multidimensional array
import firebase_admin
from firebase_admin import credentials, firestore
# firebase_admin used for initializing firebase admin using the credentials

# Initialize Firebase Admin SDK
def initialize_firebase():
    try:
        cred = credentials.Certificate(r"C:\Users\ProfessionalUseOnly\OneDrive\Desktop\New_Project_2025\fake-logo-detection-system-firebase-adminsdk-fbsvc-9780dcbed2.json")
        firebase_admin.initialize_app(cred)
        return firestore.client()
    except Exception as e:
        print(f"Error initializing Firebase: {e}")
        return None

# Function to compare uploaded image with a reference logo using template matching
def detect_fake_logo(reference_path, image_path):
    # Load the uploaded image and the reference logo image
    uploaded_img = cv2.imread(image_path)
    reference_logo = cv2.imread(reference_path, cv2.IMREAD_GRAYSCALE)
    #here reference logo (here reference logo contains rgb color of different intensity, so it) is being converted to grayscale (so that compiler had only one 
    #color) for template matching, which makes the code faster. 

    if uploaded_img is None or reference_logo is None:
        return "Error loading images"

    # Convert the uploaded image to grayscale for template matching
    uploaded_gray = cv2.cvtColor(uploaded_img, cv2.COLOR_BGR2GRAY)

    # Perform template matching
    result = cv2.matchTemplate(uploaded_gray, reference_logo, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    #finds the best match and return it's value to max_val

    # Set a threshold to decide whether the logo is genuine or fake
    threshold = 0.8  # You can adjust this threshold value
    if max_val >= threshold:
        return "Genuine"
    else:
        return "Fake"

# Function to handle file selection for reference logo
def upload_reference_logo():
    global reference_logo_path
    reference_logo_path = filedialog.askopenfilename(
        filetypes=[("Image Files", "*.jpg *.png *.jpeg *.bmp")]
    )
    if reference_logo_path:
        # Notify the user that the reference logo has been uploaded
        messagebox.showinfo("Reference Logo", "Reference logo uploaded successfully!")

# Function to handle file selection for target logo
def upload_target_logo():
    file_path = filedialog.askopenfilename(
        filetypes=[("Image Files", "*.jpg *.png *.jpeg *.bmp")]
    )
    if not file_path:
        return

    # Display selected image
    img = Image.open(file_path)
    img = img.resize((300, 300))  # Resize for display purposes
    img_tk = ImageTk.PhotoImage(img)
    # ImageTk is used so that the image processed can be converted to a format which can be accessed by tkinder so that the image can be used for GUI.
    panel.config(image=img_tk)#set image in panel
    panel.image = img_tk #prevent garbage collection

    # Check if the reference logo has been uploaded
    if not reference_logo_path:
        messagebox.showerror("Error", "Please upload the reference logo first.")
        return

    # Perform fake logo detection
    result = detect_fake_logo(reference_logo_path, file_path)

    # Save result to Firebase Firestore
    if db:
        try:
            db.collection("logo_detection_results").add({
                "file_path": file_path,
                "result": result
            })
            print("Detection result saved to Firebase.")
        except Exception as e:
            print(f"Error saving to Firebase: {e}")

    # Show detection result
    messagebox.showinfo("Detection Result", f"The uploaded logo is: {result}")

# Main GUI application
root = tk.Tk()
root.title("Fake Logo Detection")

# Initialize Firebase
db = initialize_firebase()

# Global variable to store the reference logo path
reference_logo_path = None

# Upload buttons
upload_reference_btn = tk.Button(root, text="Upload Reference Logo", command=upload_reference_logo)
upload_reference_btn.pack(pady=10)
#This will provide you with a button of Upload Reference Logo

upload_target_btn = tk.Button(root, text="Upload Logo to Detect", command=upload_target_logo)
upload_target_btn.pack(pady=10)
#This will provide you with a button of Upload Logo to Detect

# Panel to display the image
panel = tk.Label(root)
panel.pack(pady=10)

# Run the GUI event loop
root.mainloop()
