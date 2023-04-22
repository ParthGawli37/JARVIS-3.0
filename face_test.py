import cv2
import numpy as np
import face_recognition

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source, cv2.VideoCapture(0) as cap:
        print('Listening....')
        r.pause_threshold = 1
        audio = r.listen(source)

        # Initialize face recognition variables
        known_faces = [np.load('person1.npy'), np.load('person2.npy'), np.load('person3.npy')] # load saved face encodings
        known_names = ['Person 1', 'Person 2', 'Person 3'] # names of people in known_faces
        face_locations = []
        face_encodings = []
        face_names = []

        # Capture video from front camera and detect faces
        while True:
            _, frame = cap.read()
            frame_small = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small = cv2.cvtColor(frame_small, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(rgb_small, model='hog')
            face_encodings = face_recognition.face_encodings(rgb_small, face_locations)

            # Compare face encodings to known faces
            face_names = []
            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(known_faces, face_encoding)
                name = "Unknown"
                if True in matches:
                    first_match_index = matches.index(True)
                    name = known_names[first_match_index]
                face_names.append(name)

            # Display name of recognized person on video feed
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 1)
            cv2.imshow('Video', frame)

            # Exit loop if a face is recognized
            if len(face_names) > 0 and face_names[0] != 'Unknown':
                break
            cv2.waitKey(1)

    # Greet the recognized person
    name = face_names[0]
    print(f"Greetings {name}! How can I assist you today?")

    try:
        print("Recognizing.....")
        query = r.recognize_google(audio, language='en-in')
        print(f"{name} Said: {query}\n")
        c.execute("INSERT INTO voice_input (input) VALUES (?)", (query,))
        conn.commit()

    except Exception as e:
        print("Say That Again....")
        return "None"
    return query
