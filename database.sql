
CREATE DATABASE IF NOT EXISTS money_heist_analyzer;

USE money_heist_analyzer;


CREATE TABLE IF NOT EXISTS analysis_reports (
    report_id INT AUTO_INCREMENT PRIMARY KEY,
    file_name VARCHAR(255) NOT NULL,
    total_words INT NOT NULL,
    total_lines INT NOT NULL,
    total_characters INT NOT NULL,
    analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS word_frequencies (
    frequency_id INT AUTO_INCREMENT PRIMARY KEY,
    report_id INT NOT NULL,
    word VARCHAR(100) NOT NULL,
    frequency INT NOT NULL CHECK (frequency > 0),

    CONSTRAINT fk_report
        FOREIGN KEY (report_id)
        REFERENCES analysis_reports(report_id)
        ON DELETE CASCADE,

    CONSTRAINT unique_report_word
        UNIQUE (report_id, word)
);
