import tkinter as tk
from tkinter import *
import os, cv2
import shutil
import csv
import numpy as np
from PIL import ImageTk, Image
import pandas as pd
import datetime
import time
import tkinter.ttk as tkk
import tkinter.font as font
from tkinter import filedialog

haarcasecade_path = "haarcascade_frontalface_default.xml"
trainimagelabel_path = "TrainingImageLabel\\Trainner.yml"
trainimage_path = "TrainingImage"
studentdetail_path = "StudentDetails\\studentdetails.csv"
attendance_path = "Attendance"

def mark_attendance_from_photo(subject, text_to_speech):
    if subject == "":
        t = "Please enter the subject name first!"
        text_to_speech(t)
        return
    
    file_path = filedialog.askopenfilename(
        title="Select group photo for attendance",
        filetypes=[("Image files", "*.jpg *.jpeg *.png")]
    )
    
    if not file_path:
        return  # User cancelled
    
    try:
        # Load the recognizer and face detector
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        try:
            recognizer.read(trainimagelabel_path)
        except:
            e = "Model not found, please train model first"
            Notifica.configure(
                text=e,
                bg="black",
                fg="yellow",
                width=33,
                font=("times", 15, "bold"),
            )
            Notifica.place(x=20, y=250)
            text_to_speech(e)
            return
        
        face_cascade = cv2.CascadeClassifier(haarcasecade_path)
        df = pd.read_csv(studentdetail_path)
        
        # Read and process the image
        img = cv2.imread(file_path)
        if img is None:
            raise Exception("Could not read image")
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.2, 5)
        
        if len(faces) == 0:
            t = "No faces detected in the image. Please try another photo."
            text_to_speech(t)
            return
        
        # Prepare attendance record
        col_names = ["Enrollment", "Name"]
        attendance = pd.DataFrame(columns=col_names)
        
        # Process each face
        for (x, y, w, h) in faces:
            face_img = gray[y:y+h, x:x+w]
            
            # Try to recognize the face
            Id, conf = recognizer.predict(face_img)
            if conf < 70:  # Confidence threshold
                student_name = df.loc[df["Enrollment"] == Id]["Name"].values
                if len(student_name) > 0:
                    attendance.loc[len(attendance)] = [Id, student_name[0]]
                    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    cv2.putText(img, f"{Id}-{student_name[0]}", (x, y-10), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
                else:
                    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2)
                    cv2.putText(img, "Unknown", (x, y-10), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
            else:
                cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2)
                cv2.putText(img, "Unknown", (x, y-10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
        
        # Save attendance record
        if not attendance.empty:
            ts = time.time()
            date = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
            timeStamp = datetime.datetime.fromtimestamp(ts).strftime("%H-%M-%S")
            
            path = os.path.join(attendance_path, subject)
            if not os.path.exists(path):
                os.makedirs(path)
                
            fileName = f"{path}/{subject}_{date}_{timeStamp}.csv"
            attendance = attendance.drop_duplicates(["Enrollment"], keep="first")
            attendance.to_csv(fileName, index=False)
            
            # Show results
            cv2.imshow("Attendance Results", img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            
            m = f"Attendance marked for {len(attendance)} students in {subject}"
            Notifica.configure(
                text=m,
                bg="black",
                fg="yellow",
                width=33,
                relief=RIDGE,
                bd=5,
                font=("times", 15, "bold"),
            )
            text_to_speech(m)
            Notifica.place(x=20, y=250)
        else:
            t = "No recognized students in the photo"
            text_to_speech(t)
            
    except Exception as e:
        t = f"Error processing photo: {str(e)}"
        text_to_speech(t)

def subjectChoose(text_to_speech):
    def FillAttendance():
        sub = tx.get()
        now = time.time()
        future = now + 20
        print(now)
        print(future)
        if sub == "":
            t = "Please enter the subject name!!!"
            text_to_speech(t)
        else:
            try:
                recognizer = cv2.face.LBPHFaceRecognizer_create()
                try:
                    recognizer.read(trainimagelabel_path)
                except:
                    e = "Model not found,please train model"
                    Notifica.configure(
                        text=e,
                        bg="black",
                        fg="yellow",
                        width=33,
                        font=("times", 15, "bold"),
                    )
                    Notifica.place(x=20, y=250)
                    text_to_speech(e)
                facecasCade = cv2.CascadeClassifier(haarcasecade_path)
                df = pd.read_csv(studentdetail_path)
                cam = cv2.VideoCapture(0)
                font = cv2.FONT_HERSHEY_SIMPLEX
                col_names = ["Enrollment", "Name"]
                attendance = pd.DataFrame(columns=col_names)
                while True:
                    ___, im = cam.read()
                    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
                    faces = facecasCade.detectMultiScale(gray, 1.2, 5)
                    for (x, y, w, h) in faces:
                        global Id

                        Id, conf = recognizer.predict(gray[y : y + h, x : x + w])
                        if conf < 70:
                            print(conf)
                            global Subject
                            global aa
                            global date
                            global timeStamp
                            Subject = tx.get()
                            ts = time.time()
                            date = datetime.datetime.fromtimestamp(ts).strftime(
                                "%Y-%m-%d"
                            )
                            timeStamp = datetime.datetime.fromtimestamp(ts).strftime(
                                "%H:%M:%S"
                            )
                            aa = df.loc[df["Enrollment"] == Id]["Name"].values
                            global tt
                            tt = str(Id) + "-" + aa
                            attendance.loc[len(attendance)] = [
                                Id,
                                aa,
                            ]
                            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 260, 0), 4)
                            cv2.putText(
                                im, str(tt), (x + h, y), font, 1, (255, 255, 0,), 4
                            )
                        else:
                            Id = "Unknown"
                            tt = str(Id)
                            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 25, 255), 7)
                            cv2.putText(
                                im, str(tt), (x + h, y), font, 1, (0, 25, 255), 4
                            )
                    if time.time() > future:
                        break

                    attendance = attendance.drop_duplicates(
                        ["Enrollment"], keep="first"
                    )
                    cv2.imshow("Filling Attendance...", im)
                    key = cv2.waitKey(30) & 0xFF
                    if key == 27:
                        break

                ts = time.time()
                print(aa)
                attendance[date] = 1
                date = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime("%H:%M:%S")
                Hour, Minute, Second = timeStamp.split(":")
                path = os.path.join(attendance_path, Subject)
                if not os.path.exists(path):
                    os.makedirs(path)
                fileName = (
                    f"{path}/"
                    + Subject
                    + "_"
                    + date
                    + "_"
                    + Hour
                    + "-"
                    + Minute
                    + "-"
                    + Second
                    + ".csv"
                )
                attendance = attendance.drop_duplicates(["Enrollment"], keep="first")
                print(attendance)
                attendance.to_csv(fileName, index=False)

                m = "Attendance Filled Successfully of " + Subject
                Notifica.configure(
                    text=m,
                    bg="black",
                    fg="yellow",
                    width=33,
                    relief=RIDGE,
                    bd=5,
                    font=("times", 15, "bold"),
                )
                text_to_speech(m)

                Notifica.place(x=20, y=250)

                cam.release()
                cv2.destroyAllWindows()

                import csv
                import tkinter

                root = tkinter.Tk()
                root.title("Attendance of " + Subject)
                root.configure(background="black")
                cs = os.path.join(path, fileName)
                print(cs)
                with open(cs, newline="") as file:
                    reader = csv.reader(file)
                    r = 0

                    for col in reader:
                        c = 0
                        for row in col:

                            label = tkinter.Label(
                                root,
                                width=10,
                                height=1,
                                fg="yellow",
                                font=("times", 15, " bold "),
                                bg="black",
                                text=row,
                                relief=tkinter.RIDGE,
                            )
                            label.grid(row=r, column=c)
                            c += 1
                        r += 1
                root.mainloop()
                print(attendance)
            except:
                f = "No Face found for attendance"
                text_to_speech(f)
                cv2.destroyAllWindows()

    def Attf():
        sub = tx.get()
        if sub == "":
            t = "Please enter the subject name!!!"
            text_to_speech(t)
        else:
            os.startfile(f"Attendance\\{sub}")

    subject = Tk()
    subject.title("Subject...")
    subject.geometry("580x320")
    subject.resizable(0, 0)
    subject.configure(background="black")
    
    titl = tk.Label(subject, bg="black", relief=RIDGE, bd=10, font=("arial", 30))
    titl.pack(fill=X)
    
    titl = tk.Label(
        subject,
        text="Enter the Subject Name",
        bg="black",
        fg="green",
        font=("arial", 25),
    )
    titl.place(x=160, y=12)
    
    Notifica = tk.Label(
        subject,
        text="Attendance filled Successfully",
        bg="yellow",
        fg="black",
        width=33,
        height=2,
        font=("times", 15, "bold"),
    )

    # Subject Entry Frame
    entry_frame = Frame(subject, bg="black")
    entry_frame.place(x=50, y=100, width=480, height=50)
    
    sub = tk.Label(
        entry_frame,
        text="Enter Subject",
        width=10,
        height=2,
        bg="black",
        fg="yellow",
        bd=5,
        relief=RIDGE,
        font=("times new roman", 15),
    )
    sub.pack(side=LEFT, padx=5)

    tx = tk.Entry(
        entry_frame,
        width=15,
        bd=5,
        bg="black",
        fg="yellow",
        relief=RIDGE,
        font=("times", 20, "bold"),
    )
    tx.pack(side=LEFT, padx=5)

    # Button Frame (aligned horizontally)
    button_frame = Frame(subject, bg="black")
    button_frame.place(x=50, y=170, width=480, height=60)
    
    fill_a = tk.Button(
        button_frame,
        text="Fill Attendance",
        command=FillAttendance,
        bd=7,
        font=("times new roman", 15),
        bg="black",
        fg="yellow",
        height=2,
        width=15,
        relief=RIDGE,
    )
    fill_a.pack(side=LEFT, padx=10)

    photo_a = tk.Button(
        button_frame,
        text="Photo Attendance",
        command=lambda: mark_attendance_from_photo(tx.get(), text_to_speech),
        bd=7,
        font=("times new roman", 15),
        bg="black",
        fg="yellow",
        height=2,
        width=15,
        relief=RIDGE,
    )
    photo_a.pack(side=LEFT, padx=10)

    attf = tk.Button(
        button_frame,
        text="Check Sheets",
        command=Attf,
        bd=7,
        font=("times new roman", 15),
        bg="black",
        fg="yellow",
        height=2,
        width=15,
        relief=RIDGE,
    )
    attf.pack(side=LEFT, padx=10)
    
    subject.mainloop()