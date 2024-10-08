import streamlit as st
import cv2
import numpy as np
import datetime

def signup():
    st.title("Sign Up")
    st.write("Please fill out the form below to register")

    username = st.text_input("Username")
    
    st.write("Select Check-in Date:")
    check_in_date = st.date_input("")

    st.write("Select Check-out Date:")
    check_out_date = st.date_input("")
 
    # Webcam view
    st.write("Webcam view:")
    FRAME_WINDOW = st.image([])
    camera = cv2.VideoCapture(0)

    while True:
        ret, frame = camera.read()
        frame = cv2.flip(frame, 1)  # Mirror the frame
        FRAME_WINDOW.image(frame)

    if st.button("Register"):
        # Add registration logic here
        st.success("Registration successful!")

    st.write("Already have an account? Sign in here.")
    if st.button("Sign In"):
        signin()

def signin():
    st.title("Sign In")
    st.write("Please enter your username to sign in")
    username = st.text_input("Username")

    # Webcam view
    st.write("Webcam view:")
    FRAME_WINDOW = st.image([])
    camera = cv2.VideoCapture(0)

    while True:
        ret, frame = camera.read()
        frame = cv2.flip(frame, 1)  # Mirror the frame
        FRAME_WINDOW.image(frame)

    if st.button("Log In"):
        # Add login logic here
        st.success("Login successful!")

def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Choose a page", ["Sign Up", "Sign In"])

    if page == "Sign Up":
        signup()
    elif page == "Sign In":
        signin()

if __name__ == "__main__":
    main()
