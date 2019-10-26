#Copyright by YigitKader

# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import cv2
import numpy as np
import face_recognition


#take frame from camera
camera = cv2.VideoCapture(0)


frontal_face_extended=cv2.CascadeClassifier('src/haarcascade_frontalface_default.xml')
# frontal_face_extended=cv2.CascadeClassifier('cascades/frontal_face.xml')



#declare persons and images
person1_image = face_recognition.load_image_file('userpics/ygt.jpg');
person1_face_encoding = face_recognition.face_encodings(person1_image)[0]

person2_image = face_recognition.load_image_file('userpics/doganay.jpg');
person2_face_encoding = face_recognition.face_encodings(person2_image)[0]


known_face_encodings = [person1_face_encoding,person2_face_encoding]
known_face_names = ["yigit","doganay"]






#initialize variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

while True:
    # Grab a single frame of video
    ret, frame = camera.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known faces
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown.."

            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]
            face_names.append(name)



    process_this_frame = not process_this_frame


    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
        # cv2.putText(frame,"human",(left + 94,bottom - 3),font, 0.5,(255,255,255),1)



    #ISHUMAN CHECK CONTROL
    grey_ton = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY) #Convertcolor(cvtColor)

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame2 = cv2.resize(grey_ton, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame2 = small_frame[:, :, ::-1]

    faces = frontal_face_extended.detectMultiScale(rgb_small_frame2,1.1,2)

    for(x,y,w,h) in faces:
        #show frame
        x *= 4
        y *= 4
        w *= 4
        h *= 4
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2) #framei göster,sol üst ,sağ üst koordinatla,renk,kalınlık




    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# Release handle to the webcam
camera.release()
cv2.destroyAllWindows()
