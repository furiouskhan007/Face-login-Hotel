import streamlit as st
import cv2
from PIL import Image
import numpy as np
import os
import time

def home_page():
    st.title("Webcam Streamlit App")
    

def login_page():
    st.title("Login Page")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_button = st.button("Login")

    if login_button:
        # Perform login authentication here
        st.write("Logging in...")

def registration_page():
    st.title("Registration Page")
    username = st.text_input("Username")
    register_button = st.button("Register")
    
    if register_button:
        # Check if username is provided
        if not username:
            st.error("Please provide a username.")
            return

        # Initialize webcam
        cap = cv2.VideoCapture(0)

        while True:
            ret, frame = cap.read()
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Mirror the frame
            frame = cv2.flip(frame, 1)

            # Convert frame to grayscale for face detection
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

            # Load Haar Cascade for face detection
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

            # Detect faces in the frame
            faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            # Display instructions
            if len(faces) == 0:
                cv2.putText(frame, "Please look at the camera", (frame.shape[1] - 230, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
            else:
                # Save the face image
                image_path = os.path.join("images", f"{username}.jpg")
                cv2.imwrite(image_path, cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
                st.success(f"Face image registered for user: {username}")
                break

            # Display the frame
            FRAME_WINDOW.image(frame)

        # Release the webcam and close OpenCV windows
        cap.release()
        cv2.destroyAllWindows()

    FRAME_WINDOW = st.empty()
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Mirror the frame
        frame = cv2.flip(frame, 1)
        
        # Convert frame to grayscale for face detection
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        
        # Load Haar Cascade for face detection
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        # Detect faces in the frame
        faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        
        # Add semi-transparent background and text for "Please look at the camera"
        overlay = frame.copy()
        alpha = 0.4  # Transparency factor (0.0 - 1.0)
        cv2.rectangle(overlay, (frame.shape[1]-250, 0), (frame.shape[1], 50), (0, 0, 0), -1)  # Black background
        cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)
        cv2.putText(frame, "Please look at the camera", (frame.shape[1]-230, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
        
        if len(faces) == 0:
            # Add semi-transparent background and text for "Face is not detected"
            overlay = frame.copy()
            cv2.rectangle(overlay, (int(frame.shape[1]/2 - 130), frame.shape[0]-50), (int(frame.shape[1]/2 + 130), frame.shape[0]), (0, 0, 0), -1)  # Black background
            cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)
            cv2.putText(frame, "Face is not detected", (int(frame.shape[1]/2 - 80), frame.shape[0]-20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
        
        FRAME_WINDOW.image(frame)

    cap.release()
    cv2.destroyAllWindows()

def main():
    st.sidebar.title("Navigation")
    menu_selection = st.sidebar.radio("Go to", ["Home", "Login", "Register"])

    if menu_selection == "Home":
        home_page()
    elif menu_selection == "Login":
        login_page()
    elif menu_selection == "Register":
        registration_page()

if __name__ == "__main__":
    main()
