import psycopg2
import logging

logging.basicConfig(level=logging.INFO)

# Connect to the PostgreSQL database
# conn = psycopg2.connect(
#     database="frames_get",
#     user="postgres",
#     password="root",
#     host="localhost",
#     port="5432",
# )

def store_processed_frames(task_id, frame_id, time_taken, worker_id, frame_data):
    try:
        connection = psycopg2.connect(
            database="frames_get",
            user="postgres",
            password="root",
            host="localhost",
            port="5432")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO frames(task_id,frame_id,time_taken, worker_id, image) VALUES (%s,%s, %s, %s, %s)", (task_id,frame_id, time_taken, worker_id, frame_data))
        connection.commit()
    except (Exception, psycopg2.Error) as error:
        logging.info("Failed to insert processed frame into database", error)
    finally:
    # closing database connection.
        if connection:
            cursor.close()
            connection.close()

def get_frame_count(task_id):
    try:
        connection = psycopg2.connect(
            database="frames_get",
            user="postgres",
            password="root",
            host="localhost",
            port="5432")
        cursor = connection.cursor()
        query = "SELECT COUNT(*) FROM save_frames WHERE task_id = %s"

    # Execute the query with the primary key value
        cursor.execute(query, (task_id,))
        count = cursor.fetchone()[0]
    except (Exception, psycopg2.Error) as error:
        logging.info("Failed to read from database", error)
    finally:
    # closing database connection.
        if connection:
            cursor.close()
            connection.close()
        return count
    
def get_saved_frame_count(task_id):
    try:
        connection = psycopg2.connect(
            database="frames_get",
            user="postgres",
            password="root",
            host="localhost",
            port="5432")
        cursor = connection.cursor()
        query = "SELECT COUNT(*) FROM frames WHERE task_id = %s"

    # Execute the query with the primary key value
        cursor.execute(query, (task_id,))
        count = cursor.fetchone()[0]
    except (Exception, psycopg2.Error) as error:
        logging.info("Failed to read from database", error)
    finally:
    # closing database connection.
        if connection:
            cursor.close()
            connection.close()
    return count

def get_statistics(task_id):
    try:
        connection = psycopg2.connect(
            database="frames_get",
            user="postgres",
            password="root",
            host="localhost",
            port="5432")
        cursor = connection.cursor()
        query = query = "SELECT worker_id, AVG(time_taken), COUNT(*) FROM frames WHERE task_id = %s GROUP BY worker_id "

    # Execute the query with the primary key value
        cursor.execute(query, (task_id,))
        stats = []
        for record in cursor:
            worker_id = record[0]
            time_taken = record[1]
            frames_processed = record[2]
            stats.append({'worker_id':worker_id , 'time_taken' : time_taken, 'frames_processed':frames_processed})
    except (Exception, psycopg2.Error) as error:
        logging.info("Failed to read from database", error)
    finally:
    # closing database connection.
        if connection:
            cursor.close()
            connection.close()
    return stats