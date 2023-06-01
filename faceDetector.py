import numpy as np
import cv2
import dlib

def get_features(frame_bytes):

    predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
    try:
        # Convert the received data  to a NumPy array
        frame = np.frombuffer(frame_bytes, dtype=np.uint8)
        frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)

        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        detector = dlib.get_frontal_face_detector()
        faces = detector(gray)

        # Iterate over the detected faces and extract the facial landmarks
        for face in faces:
            landmarks = predictor(gray, face)
            points = []
            for n in range(0, 68):
                x = landmarks.part(n).x
                y = landmarks.part(n).y
                points.append((x, y))

            # Compute the Delaunay triangulation on the extracted landmarks
            rect = (0, 0, frame.shape[1], frame.shape[0])
            subdiv = cv2.Subdiv2D(rect)
            for point in points:
                subdiv.insert(point)
            triangle_list = subdiv.getTriangleList()

            # Draw the Delaunay triangles on the frame
            for t in triangle_list:
                pt1 = (int(t[0]), int(t[1]))
                pt2 = (int(t[2]), int(t[3]))
                pt3 = (int(t[4]), int(t[5]))
                cv2.line(frame, pt1, pt2, (0, 255, 0), 1, cv2.LINE_AA)
                cv2.line(frame, pt2, pt3, (0, 255, 0), 1, cv2.LINE_AA)
                cv2.line(frame, pt3, pt1, (0, 255, 0), 1, cv2.LINE_AA)

        # Encode the frame as JPEG
        _, encoded_frame = cv2.imencode('.jpg', frame)
        processed_frame_data = encoded_frame.tobytes()

    except Exception as e:
        # Send the original frame back
        processed_frame_data = frame_bytes

    # Send the processed frame data back to the main node
    return(processed_frame_data)
