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


def load_mission_text():
    try:
        with open(TEXT_SOURCE, "r", encoding="utf-8") as source:
            return source.read()

    except FileNotFoundError:
        print("Text source not found. Check sample.txt.")
        return None

    except OSError as error:
        print(f"Unable to read the text source: {error}")
        return None


def calculate_text_intelligence(text):
    tokens = re.findall(r"\b[\w']+\b", text.lower())
    text_lines = text.splitlines()
    character_total = len(text.replace("\r", "").replace("\n", ""))

    frequency_map = Counter(tokens)

    return {
        "word_count": len(tokens),
        "line_count": len(text_lines),
        "character_count": character_total,
        "word_frequency": frequency_map
    }


def print_intelligence_report(report):
    print("\n" + "=" * 50)
    print("       THE PROFESSOR'S INTELLIGENCE REPORT")
    print("=" * 50)

    print(f"Total words      : {report['word_count']}")
    print(f"Total lines      : {report['line_count']}")
    print(f"Total characters : {report['character_count']}")

    print("\n--- TOP 3 MOST FREQUENT WORDS ---")

    for word, count in report["word_frequency"].most_common(3):
        print(f"{word:<20} : {count}")

    print("=" * 50)


def run_text_analysis():
    print("\nPreparing the text analysis...")

    text = load_mission_text()

    if text is None:
        return

    report = calculate_text_intelligence(text)
    print_intelligence_report(report)

    source_name = os.path.basename(TEXT_SOURCE)

    print("\n--- DATABASE STORAGE ---")

    if save_mission_report(source_name, report):
        print("The intelligence report has been secured.")
    else:
        print("Unable to save the report.")


def show_mission_archive():
    archive = retrieve_mission_archive()

    print("\n" + "=" * 75)
    print("                    MISSION ARCHIVE")
    print("=" * 75)

    if not archive:
        print("No reports found, or the database is unavailable.")
        return

    for record in archive:
        print(f"\nReport ID       : {record['report_id']}")
        print(f"File name       : {record['file_name']}")
        print(f"Total words     : {record['total_words']}")
        print(f"Total lines     : {record['total_lines']}")
        print(f"Total characters: {record['total_characters']}")
        print(f"Analyzed at     : {record['analyzed_at']}")

    print("\n" + "=" * 75)


def choose_archive_report():
    archive = retrieve_mission_archive()

    if not archive:
        print("\nNo saved reports found, or the database is unavailable.")
        return None

    print("\n--- AVAILABLE REPORTS ---")

    for record in archive:
        print(
            f"ID: {record['report_id']} | "
            f"File: {record['file_name']} | "
            f"Words: {record['total_words']} | "
            f"Date: {record['analyzed_at']}"
        )

    try:
        selected_id = int(input("\nEnter the report ID: "))

    except ValueError:
        print("Enter a valid numeric report ID.")
        return None

    for record in archive:
        if record["report_id"] == selected_id:
            return selected_id

    print("The selected report ID does not exist.")
    return None


def investigate_word_frequency():
    print("\n--- WORD FREQUENCY INVESTIGATION ---")

    report_id = choose_archive_report()

    if report_id is None:
        return

    target_word = input("Enter the word to investigate: ").strip().lower()

    if not target_word:
        print("Enter a word before searching.")
        return

    if not re.fullmatch(r"[\w']+", target_word):
        print("Enter one valid word without spaces or punctuation.")
        return

    frequency = investigate_saved_word(report_id, target_word)

    if frequency is None:
        print("The search could not be completed.")
    elif frequency == 0:
        print(f"'{target_word}' was not found in Report ID {report_id}.")
    else:
        print(f"\nWord      : {target_word}")
        print(f"Frequency : {frequency}")
        print(f"Report ID : {report_id}")


def reveal_top_words():
    print("\n--- WORD FREQUENCY RANKINGS ---")

    report_id = choose_archive_report()

    if report_id is None:
        return

    rankings = retrieve_word_rankings(report_id)

    if not rankings:
        print("No frequency records found, or the database is unavailable.")
        return

    try:
        number_of_words = int(input("How many top words should be displayed? "))

        if number_of_words <= 0:
            print("Enter a number greater than zero.")
            return

    except ValueError:
        print("Enter a valid whole number.")
        return

    print(f"\n--- TOP {number_of_words} WORDS IN REPORT {report_id} ---")

    for item in rankings[:number_of_words]:
        print(f"{item['word']:<25} : {item['frequency']}")


def print_control_room():
    print("\n" + "=" * 50)
    print("       THE PROFESSOR'S CONTROL ROOM")
    print("=" * 50)
    print("1. Analyze text file")
    print("2. View mission archive")
    print("3. Investigate a word")
    print("4. View word frequency rankings")
    print("5. Exit")
    print("=" * 50)


def launch_control_room():
    while True:
        print_control_room()

        selection = input("Your choice, Professor: ").strip()

        if selection == "1":
            run_text_analysis()

        elif selection == "2":
            show_mission_archive()

        elif selection == "3":
            investigate_word_frequency()

        elif selection == "4":
            reveal_top_words()

        elif selection == "5":
            print("\nThe mission is complete. Bella Ciao!")
            break

        else:
            print("\nInvalid choice. Select an option from 1 to 5.")


if __name__ == "__main__":
    launch_control_room()