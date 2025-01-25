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
        cred = credentials.Certificate(r"C:\Users\User\Desktop\Fakelogodetection\fake-logo-7a57d-firebase-adminsdk-fbsvc-d86692cfa0.json")
        firebase_admin.initialize_app(cred)
        return firestore.client()
    except Exception as e:
        print(f"Error initializing Firebase: {e}")
        return None

# Function to detect fake logos (stub function; replace with your logic)
def detect_fake_logo(image_path):
    # Placeholder for fake logo detection logic
    # Replace this with your algorithm to detect fake logos
    # Example: comparing the uploaded logo with a reference logo using feature matching
    
    # For now, just return a dummy result
    return "Fake" if "fake" in image_path.lower() else "Genuine"

# Function to handle file selection
def upload_file():
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

    # Perform fake logo detection
    result = detect_fake_logo(file_path)

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

# Upload button
upload_btn = tk.Button(root, text="Upload Logo", command=upload_file)
upload_btn.pack(pady=20)

# Panel to display the image
panel = tk.Label(root)
panel.pack(pady=10)

# Run the GUI event loop
root.mainloop()
