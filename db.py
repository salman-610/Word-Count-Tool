import os
import mysql.connector
from dotenv import load_dotenv
from mysql.connector import Error

load_dotenv()


def connect_database():
    try:
        password = os.getenv("MYSQL_PASSWORD")

        if not password:
            print("MySQL password not found. Check your .env file.")
            return None

        return mysql.connector.connect(
            host="localhost",
            user="root",
            password=password,
            database="money_heist_analyzer"
        )

    except Error as error:
        print(f"Database connection failed: {error}")
        return None


def save_mission_report(file_name, results):
    connection = connect_database()

    if connection is None:
        return False

    cursor = None

    try:
        cursor = connection.cursor()

        report_query = """
            INSERT INTO analysis_reports
            (file_name, total_words, total_lines, total_characters)
            VALUES (%s, %s, %s, %s)
        """

        report_values = (
            file_name,
            results["word_count"],
            results["line_count"],
            results["character_count"]
        )

        cursor.execute(report_query, report_values)
        report_id = cursor.lastrowid

        frequency_query = """
            INSERT INTO word_frequencies
            (report_id, word, frequency)
            VALUES (%s, %s, %s)
        """

        frequency_values = [
            (report_id, word, count)
            for word, count in results["word_frequency"].items()
        ]

        if frequency_values:
            cursor.executemany(frequency_query, frequency_values)

        connection.commit()
        print(f"Analysis saved successfully. Report ID: {report_id}")
        return True

    except Error as error:
        connection.rollback()
        print(f"Error saving analysis: {error}")
        return False

    finally:
        if cursor is not None:
            cursor.close()

        connection.close()


def retrieve_mission_archive():
    connection = connect_database()

    if connection is None:
        return []

    cursor = None

    try:
        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT report_id, file_name, total_words,
                   total_lines, total_characters, analyzed_at
            FROM analysis_reports
            ORDER BY report_id DESC
        """

        cursor.execute(query)
        return cursor.fetchall()

    except Error as error:
        print(f"Error retrieving reports: {error}")
        return []

    finally:
        if cursor is not None:
            cursor.close()

        connection.close()


def retrieve_word_rankings(report_id):
    connection = connect_database()

    if connection is None:
        return []

    cursor = None

    try:
        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT word, frequency
            FROM word_frequencies
            WHERE report_id = %s
            ORDER BY frequency DESC, word ASC
        """

        cursor.execute(query, (report_id,))
        return cursor.fetchall()

    except Error as error:
        print(f"Error retrieving word rankings: {error}")
        return []

    finally:
        if cursor is not None:
            cursor.close()

        connection.close()


def investigate_saved_word(report_id, word):
    connection = connect_database()

    if connection is None:
        return None

    cursor = None

    try:
        cursor = connection.cursor()

        query = """
            SELECT frequency
            FROM word_frequencies
            WHERE report_id = %s AND word = %s
        """

        cursor.execute(query, (report_id, word.lower()))
        result = cursor.fetchone()

        return result[0] if result else 0

    except Error as error:
        print(f"Error searching word frequency: {error}")
        return None

    finally:
        if cursor is not None:
            cursor.close()

        connection.close()


if __name__ == "__main__":
    connection = connect_database()

    if connection and connection.is_connected():
        print("Database connection successful!")
        connection.close()
        print("Connection closed successfully.")