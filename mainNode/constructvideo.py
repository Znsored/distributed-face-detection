import cv2
import psycopg2
import numpy as np

def construct_vid(task_id):
    # Database connection details
    db_name = 'frames_get'
    db_user = 'postgres'
    db_password = 'root'

    # Connect to the database
    connection = psycopg2.connect(database=db_name, user=db_user, password=db_password)
    cursor = connection.cursor()

    # Execute the query
    cursor.execute( "SELECT frame_id, image FROM frames WHERE task_id=(%s) ORDER BY frame_id",(task_id,))

    # Initialize variables
    frame_count = 0
    frames = []

    # Iterate over the database records
    for record in cursor:
        frame_id = record[0]
        image_bytes = record[1]

        # Convert the image bytes to a NumPy array
        nparr = np.frombuffer(image_bytes, np.uint8)

        # Decode the NumPy array as an image using OpenCV
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Add the frame ID and image to the list
        frames.append((frame_id, image))

        # Increment frame count
        frame_count += 1

    # Release the database cursor and close the connection
    cursor.close()
    connection.close()

    # Specify the desired frame size
    frame_width = 1280
    frame_height = 720

    # Create a VideoWriter object to construct the video
    output_file = 'output_video.avi'
    frame_rate = 30
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    output_video = cv2.VideoWriter(output_file, fourcc, frame_rate, (frame_width, frame_height))

    # Iterate over the frames, resize them, and add them to the video
    for frame_id, image in frames:
        resized_image = cv2.resize(image, (frame_width, frame_height))
        output_video.write(resized_image)

    # Release the VideoWriter
    output_video.release()

    print(f"Video constructed successfully. Output file: {output_file}")
