import streamlit as st
import face_recognition
import cv2
import pickle
import os
from datetime import datetime

class Dlib_Face_Unlock:
    def __init__(self):
        self.labels_ids = {}
        self.known_faces = []
        self.load_known_faces()

    def load_known_faces(self):
        if os.path.exists('labels.pickle') and os.path.exists('KnownFace.pickle'):
            with open('labels.pickle', 'rb') as f:
                self.labels_ids = pickle.load(f)

            with open('KnownFace.pickle', 'rb') as f:
                self.known_faces = pickle.load(f)
        else:
            print("No label.pickle file detected, will create required pickle files")

        if not self.labels_ids:
            self.current_id = 0
            self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))
            self.image_dir = os.path.join(self.BASE_DIR, 'images')

            if not os.path.exists(self.image_dir):
                os.makedirs(self.image_dir)

            for root, dirs, files in os.walk(self.image_dir):
                for file in files:
                    if file.endswith('png') or file.endswith('jpg'):
                        path = os.path.join(root, file)
                        label = os.path.basename(os.path.dirname(path)).replace(' ', '-').lower()
                        if label not in self.labels_ids:
                            self.labels_ids[label] = self.current_id
                            self.current_id += 1

            if self.labels_ids:
                with open('labels.pickle', 'wb') as f:
                    pickle.dump(self.labels_ids, f)

                for i in self.labels_ids:
                    noOfImgs = len([filename for filename in os.listdir(os.path.join('images', i))
                                    if os.path.isfile(os.path.join('images', i, filename))])
                    for imgNo in range(1, (noOfImgs + 1)):
                        directory = os.path.join(self.image_dir, i, str(imgNo) + '.png')
                        img = face_recognition.load_image_file(directory)
                        img_encoding = face_recognition.face_encodings(img)[0]
                        self.known_faces.append([i, img_encoding])

                if self.known_faces:
                    with open('KnownFace.pickle', 'wb') as f:
                        pickle.dump(self.known_faces, f)

    def recognize_face(self, frame):
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces([face[1] for face in self.known_faces], face_encoding)
            name = "Unknown"
            if True in matches:
                first_match_index = matches.index(True)
                name = self.known_faces[first_match_index][0]
            face_names.append(name)

        return face_names

def register(name, check_in, check_out):
    image_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'images', name.lower())
    os.makedirs(image_dir, exist_ok=True)

    numberOfFile = len([filename for filename in os.listdir(image_dir)]) + 1

    cap = cv2.VideoCapture(0)
    cv2.namedWindow("test")

    while True:
        ret, frame = cap.read()
        cv2.imshow("test", frame)
        if not ret:
            break
        k = cv2.waitKey(1)

        if k % 256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            cap.release()
            cv2.destroyAllWindows()
            break
        elif k % 256 == 32:
            # SPACE pressed
            img_name = str(numberOfFile) + ".png"
            cv2.imwrite(os.path.join(image_dir, img_name), frame)
            print("{} written!".format(img_name))
            cap.release()
            cv2.destroyAllWindows()
            break

    # Store check-in and check-out time
    with open('check_in_out_log.txt', 'a') as f:
        f.write(f"{name}, {check_in.strftime('%Y-%m-%d %H:%M:%S')}, {check_out.strftime('%Y-%m-%d %H:%M:%S')}\n")

def main():
    st.image("OK.png", width=100)
    st.title("ToT - Truly Open & Trusted")

    menu = ["Home", "Login", "Registration"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.subheader("Welcome to ToT!")
        st.write("Please select an option from the side menu.")

    elif choice == "Login":
        st.header("Login")
        dfu = Dlib_Face_Unlock()
        name = st.text_input("Enter your username")
        if name:
            if name.lower() in [label.lower() for label in dfu.labels_ids]:
                st.info("Please look at the camera to perform face recognition...")
                cap = cv2.VideoCapture(0)
                while True:
                    ret, frame = cap.read()
                    if not ret:
                        break

                    face_names = dfu.recognize_face(frame)
                    if name.lower() in [n.lower() for n in face_names]:
                        st.success(f"Welcome, {name}!")
                        # Display check-in and check-out dates
                        with open('check_in_out_log.txt', 'r') as f:
                            lines = f.readlines()
                            for line in lines:
                                info = line.split(',')
                                if info[0].strip().lower() == name.lower():
                                    st.write(f"Check-in: {info[1]}, Check-out: {info[2]}")
                        break

                    # Display the resulting frame
                    cv2.imshow('Frame', frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break

                # When everything done, release the capture
                cap.release()
                cv2.destroyAllWindows()
            else:
                st.warning("Not registered")

    elif choice == "Registration":
        st.header("Registration")
        reg_name = st.text_input("Enter your name for registration")
        check_in = st.date_input("Select check-in date")
        check_out = st.date_input("Select check-out date")

        if st.button("Register"):
            if reg_name:
                register(reg_name, check_in, check_out)
                st.success(f"{reg_name} registered successfully!")

if __name__ == "__main__":
    main()
