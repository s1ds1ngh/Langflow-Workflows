import psycopg2
from psycopg2 import Error
from src.utils.config.settings import settings


def execute_query(query, level=None):
    try:
        # Establish database connection
        connection = psycopg2.connect(
            host='localhost',  # Replace with your database host
            user=settings.DB_USER,  # Replace with your database username
            password=settings.DB_PASSWORD,  # Replace with your database password
            database=settings.QUESTIONS_DB  # Replace with your database name
        )

        if connection:
            cursor = connection.cursor()

            # Modify the query to include a WHERE clause based on the level
            if level:
                query += " WHERE difficulty_level = %s"
                cursor.execute(query, (level,))
            else:
                cursor.execute(query)

            # Fetch all results
            result = cursor.fetchall()

            # Convert the result into a dictionary format
            columns = [desc[0] for desc in cursor.description]  # Fetch column names
            result_dict = [dict(zip(columns, row)) for row in result]

            return {
                "success": True,
                "data": result_dict
            }

    except Error as e:
        return {
            "success": False,
            "error": str(e)
        }

    finally:
        if 'connection' in locals() and connection:
            cursor.close()
            connection.close()


def extract_questions(data):
    # Extract the 'question_text' from each dictionary in the list and return as an array
    return [item['question_text'] for item in data]


def merge_questions(gen_ques_input: dict, db_ques_input: list):
    quest = ""
    return quest
