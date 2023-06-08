import cv2
import psycopg2
import numpy as np
import subprocess

def construct_vid(task_id):
    # Database connection details
    db_name = 'frames_get'
    db_user = 'postgres'
    db_password = 'root'

    # Connect to the database
    connection = psycopg2.connect(database=db_name, user=db_user, password=db_password)
    cursor = connection.cursor()

    # Execute the query
    cursor.execute("SELECT  image FROM frames WHERE task_id =(%s) ORDER BY frame_id",(task_id,))

    # Initialize variables
    frames = []

    # Iterate over the database records
    for record in cursor:

        image_bytes = record[0]

        # Convert the bytea image to a NumPy array
        nparr = np.frombuffer(image_bytes, np.uint8)

        # Decode the NumPy array as an image using OpenCV
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Process the image here (if required)
        processed_image = image

        # Add the processed image to the list
        frames.append(processed_image)

    # Release the database cursor and close the connection
    cursor.close()
    connection.close()

    # Construct the video using FFmpeg
    construct_video(frames)

def construct_video(input_images):
    # Get the frame width and height from the first image
    frame_width = input_images[0].shape[1]
    frame_height = input_images[0].shape[0]
    output_file='./mainNode/static/video.mp4'
    # Construct the FFmpeg command
    command = [
        'ffmpeg',
        '-r', str(30),
        '-f', 'rawvideo',
        '-s', f'{frame_width}x{frame_height}',
        '-pix_fmt', 'bgr24',
        '-i', '-',
        '-c:v', 'libx264',
        '-pix_fmt', 'yuv420p',
        '-crf', '18',
        '-y',
        output_file
    ]

    # Start the FFmpeg process
    ffmpeg_process = subprocess.Popen(command, stdin=subprocess.PIPE)

    # Write the input images to the FFmpeg process
    for image in input_images:
        ffmpeg_process.stdin.write(image.tobytes())

    # Close the FFmpeg process
    ffmpeg_process.stdin.close()
    ffmpeg_process.wait()

    print(f"Video constructed successfully. Output file: {output_file}")

