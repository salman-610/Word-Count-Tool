Word Count Tool — Professor's Control Room

Overview

The Word Count Tool is a Python application that examines a text file and records its statistics in a MySQL database. Its command-line interface is inspired by the planning room in Money Heist.

The application measures text length, identifies frequently used words, and maintains a history of completed analyses. Users can revisit previous reports without analyzing the file again.

Capabilities

- Count words, lines, and characters.
- Calculate the frequency of each word.
- Display the three most frequent words after an analysis.
- Store analysis summaries and word frequencies in MySQL.
- Browse previously saved reports.
- Search for a particular word in a selected report.
- Retrieve the most frequent words from any saved report.

Technology Stack

- Python 3
- MySQL
- MySQL Connector/Python
- python-dotenv

Folder Layout


word_count_tool/
├── main.py
├── db.py
├── sample.txt
├── requirements.txt
├── README.md
├── .gitignore
└── .env


The '.env' file contains local database credentials and must not be published.

Prerequisites

Install Python 3 and MySQL Server. MySQL Workbench can be used to create the database and inspect stored reports.

Database Initialization

Execute this SQL in MySQL Workbench:


CREATE DATABASE money_heist_analyzer;

USE money_heist_analyzer;

CREATE TABLE analysis_reports (
    report_id INT AUTO_INCREMENT PRIMARY KEY,
    file_name VARCHAR(255) NOT NULL,
    total_words INT NOT NULL,
    total_lines INT NOT NULL,
    total_characters INT NOT NULL,
    analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE word_frequencies (
    frequency_id INT AUTO_INCREMENT PRIMARY KEY,
    report_id INT NOT NULL,
    word VARCHAR(100) NOT NULL,
    frequency INT NOT NULL,
    FOREIGN KEY (report_id)
        REFERENCES analysis_reports(report_id)
        ON DELETE CASCADE
);


The first table stores the overall results for each analysis. The second stores each word's frequency and connects it to its report through 'report_id'.

Installation and Configuration

Install the required packages from the project directory:


py -m pip install -r requirements.txt


Add your local MySQL password to '.env':

MYSQL_PASSWORD=your_actual_mysql_password


Update the database connection settings in 'db.py' if your MySQL username or database configuration differs.

Keep '.env' in '.gitignore'. Never publish actual database credentials.

Running the Application

Place the text you want to examine in 'sample.txt'.

Start the application:


py main.py


The Professor's Control Room provides these operations:

| Selection | Operation |
|---|---|
| 1 | Analyze the text file and save a report |
| 2 | Browse saved analysis reports |
| 3 | Search for a word in a chosen report |
| 4 | Display the top N words in a report |
| 5 | Exit |

Each analysis creates a new database report. Previous reports are retained for later review.

Example Analysis

The current sample file produces these results:

| Measurement | Result |
|---|---:|
| Words | 845 |
| Lines | 23 |
| Characters excluding line breaks | 5,015 |

The three most frequent words are:

| Word | Occurrences |
|---|---:|
| the | 83 |
| and | 43 |
| a | 19 |

These values describe the current sample file and will change when its contents change.

Learning Outcomes

This project demonstrates Python file reading, regular expressions, text processing, frequency counting, exception handling, modular programming, SQL queries, and relational database integration.

Author

Salman A
