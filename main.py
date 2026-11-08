
import os
import re
from collections import Counter

from db import (
    save_mission_report,
    retrieve_mission_archive,
    retrieve_word_rankings,
    investigate_saved_word
)


PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
TEXT_SOURCE = os.path.join(PROJECT_DIR, "sample.txt")




def retrieve_source_content():
    try:
        with open(TEXT_SOURCE, "r", encoding="utf-8") as source:
            return source.read()

    except FileNotFoundError:
        print("Source file is missing. Please check sample.txt.")
        return None

    except OSError as error:
        print(f"Unable to access the source file: {error}")
        return None




def generate_text_metrics(content):
    words = re.findall(r"\b[\w']+\b", content.lower())

    lines = content.splitlines()

    characters = len(content.replace("\r", "").replace("\n", ""))

    keyword_counts = Counter(words)

    return {
        "word_count": len(words),
        "line_count": len(lines),
        "character_count": characters,
        "word_frequency": keyword_counts
    }




def display_analysis_briefing(metrics):
    print("\n" + "=" * 50)
    print("       THE PROFESSOR'S INTELLIGENCE REPORT")
    print("=" * 50)

    print(f"Total words      : {metrics['word_count']}")
    print(f"Total lines      : {metrics['line_count']}")
    print(f"Total characters : {metrics['character_count']}")

    print("\n--- TOP 3 MOST FREQUENT WORDS ---")

    for word, count in metrics["word_frequency"].most_common(3):
        print(f"{word:<20} : {count}")

    print("=" * 50)




def execute_document_analysis():
    print("\nPreparing the document analysis...")

    content = retrieve_source_content()

    if content is None:
        return

    metrics = generate_text_metrics(content)

    display_analysis_briefing(metrics)

    file_label = os.path.basename(TEXT_SOURCE)

    print("\n--- DATABASE STORAGE ---")

    if save_mission_report(file_label, metrics):
        print("The analysis report has been successfully secured.")
    else:
        print("The report could not be saved to the database.")



def display_saved_reports():
    reports = retrieve_mission_archive()

    print("\n" + "=" * 75)
    print("                    MISSION ARCHIVE")
    print("=" * 75)

    if not reports:
        print("No saved reports are available.")
        return

    for report in reports:
        print(f"\nReport ID       : {report['report_id']}")
        print(f"File name       : {report['file_name']}")
        print(f"Total words     : {report['total_words']}")
        print(f"Total lines     : {report['total_lines']}")
        print(f"Total characters: {report['total_characters']}")
        print(f"Analyzed at     : {report['analyzed_at']}")

    print("\n" + "=" * 75)




def select_report_reference():
    reports = retrieve_mission_archive()

    if not reports:
        print("\nNo saved reports are available.")
        return None

    print("\n--- AVAILABLE REPORTS ---")

    for report in reports:
        print(
            f"ID: {report['report_id']} | "
            f"File: {report['file_name']} | "
            f"Words: {report['total_words']} | "
            f"Date: {report['analyzed_at']}"
        )

    try:
        report_reference = int(input("\nEnter the report ID: ").strip())

    except ValueError:
        print("Invalid input. Please enter a numeric report ID.")
        return None

    for report in reports:
        if report["report_id"] == report_reference:
            return report_reference

    print("The selected report ID was not found.")
    return None




def search_report_keyword():
    print("\n--- WORD FREQUENCY INVESTIGATION ---")

    report_reference = select_report_reference()

    if report_reference is None:
        return

    keyword = input("Enter the word to investigate: ").strip().lower()

    if not keyword:
        print("Please enter a word to continue.")
        return

    if not re.fullmatch(r"[\w']+", keyword):
        print("Enter one valid word without spaces or punctuation.")
        return

    occurrence = investigate_saved_word(report_reference, keyword)

    if occurrence is None:
        print("Unable to complete the keyword search.")

    elif occurrence == 0:
        print(f"'{keyword}' was not found in Report ID {report_reference}.")

    else:
        print(f"\nWord      : {keyword}")
        print(f"Frequency : {occurrence}")
        print(f"Report ID : {report_reference}")


def display_keyword_leaderboard():
    print("\n--- WORD FREQUENCY RANKINGS ---")

    report_reference = select_report_reference()

    if report_reference is None:
        return

    rankings = retrieve_word_rankings(report_reference)

    if not rankings:
        print("No word frequency records are available.")
        return

    try:
        display_limit = int(
            input("How many top words should be displayed? ").strip()
        )

        if display_limit <= 0:
            print("Enter a number greater than zero.")
            return

    except ValueError:
        print("Please enter a valid whole number.")
        return

    print(f"\n--- TOP {display_limit} WORDS IN REPORT {report_reference} ---")

    for entry in rankings[:display_limit]:
        print(f"{entry['word']:<25} : {entry['frequency']}")



def render_command_interface():
    print("\n" + "=" * 50)
    print("       THE PROFESSOR'S CONTROL ROOM")
    print("=" * 50)
    print("1. Analyze text file")
    print("2. View mission archive")
    print("3. Investigate a word")
    print("4. View word frequency rankings")
    print("5. Exit")
    print("=" * 50)


def start_professor_console():
    while True:
        render_command_interface()

        selection = input("Your choice, Professor: ").strip()

        if selection == "1":
            execute_document_analysis()

        elif selection == "2":
            display_saved_reports()

        elif selection == "3":
            search_report_keyword()

        elif selection == "4":
            display_keyword_leaderboard()

        elif selection == "5":
            print("\nThe mission is complete. Bella Ciao!")
            break

        else:
            print("\nInvalid choice. Select an option from 1 to 5.")


if __name__ == "__main__":
    start_professor_console()
