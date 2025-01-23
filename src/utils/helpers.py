import psycopg2
from src.utils.config.settings import settings
from psycopg2.extras import RealDictCursor


def execute_query(query, params=None):
    """
    Execute a database query with optional parameters.
    Returns a dictionary containing the success status and data or error message.
    """
    try:
        # Establish database connection
        connection = psycopg2.connect(
            host='localhost',  # Replace with your database host
            user=settings.DB_USER,  # Replace with your database username
            password=settings.DB_PASSWORD,  # Replace with your database password
            database=settings.QUESTIONS_DB  # Replace with your database name
        )
        cursor = connection.cursor(cursor_factory=RealDictCursor)

        # Execute the query with parameters
        cursor.execute(query, params)

        # Fetch all results
        result = cursor.fetchall()

        return {
            "success": True,
            "data": result
        }

    except psycopg2.Error as e:
        return {
            "success": False,
            "error": str(e)
        }

    finally:
        # Ensure resources are closed properly
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()


def extract_questions(data):
    # Extract the 'question_text' from each dictionary in the list and return as an array
    return [item['question_text'] for item in data]


def merge_questions(gen_ques_input: dict, db_ques_input: list):
    quest = ""
    return quest
