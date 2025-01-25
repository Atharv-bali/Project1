import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2
import numpy as np
import firebase_admin
from firebase_admin import credentials, firestore

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

    if uploaded_img is None or reference_logo is None:
        return "Error loading images"

    # Convert the uploaded image to grayscale for template matching
    uploaded_gray = cv2.cvtColor(uploaded_img, cv2.COLOR_BGR2GRAY)

    # Perform template matching
    result = cv2.matchTemplate(uploaded_gray, reference_logo, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

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
    panel.config(image=img_tk)
    panel.image = img_tk

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

upload_target_btn = tk.Button(root, text="Upload Logo to Detect", command=upload_target_logo)
upload_target_btn.pack(pady=10)

# Panel to display the image
panel = tk.Label(root)
panel.pack(pady=10)

# Run the GUI event loop
root.mainloop()
