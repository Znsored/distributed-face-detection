import cv2
import psycopg2
import numpy as np

# Database connection details
db_name = 'frames_get'
db_user = 'postgres'
db_password = 'root'

# Connect to the database
connection = psycopg2.connect(database=db_name, user=db_user, password=db_password)
cursor = connection.cursor()

# SQL query to fetch image data from the database
sql_query = "SELECT image FROM frames"

# Execute the query
cursor.execute(sql_query)

# Iterate over the database records
for record in cursor:
    image_bytes = record[0]

    # Convert the image bytes to a NumPy array
    nparr = np.frombuffer(image_bytes, np.uint8)

    # Decode the NumPy array as an image using OpenCV
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Display the image
    cv2.imshow('Image', image)
    cv2.waitKey(0)  # Wait for any key press
    cv2.destroyAllWindows()

# Release the database cursor and close the connection
cursor.close()
connection.close()
