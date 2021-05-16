""" this script extracts the necessary stuff out of calvins questions csv file..."""

import csv

INFILE = "./quiz_questions/quiz_questions.csv"
OUTFILE = "./quiz_questions/clean_quiz_questions.csv"

def clean_question_file():
    with open(INFILE) as csv_file:
        reader = csv.reader(csv_file, delimiter=",")

        reader = list(reader)

        column_names = reader[0]

        columns = {}

        for index, name in enumerate(column_names):
            columns[name] = index

        row_list = []
        for row in reader[1:]:
            if row[columns["Type"]] == "Multi-choice":
                new_row = [
                    row[columns["Question"]],
                    row[columns["Answer"]],
                    row[columns["Option1"]],
                    row[columns["Option2"]],
                    row[columns["Option3"]],
                ]
                row_list.append(new_row)

    with open(OUTFILE, "w") as csv_file:
        writer = csv.writer(csv_file, delimiter=",")

        columns = [
            "question",
            "answer",
            "wrong_1",
            "wrong_2",
            "wrong_3"
        ]

        writer.writerow(columns)

        for row in row_list:
            writer.writerow(row)


def main():
    """ clean calvins questions """
    clean_question_file()
    print("Cleaned - {}\nCreated - {}".format(INFILE, OUTFILE))


if __name__ == "__main__":
    main()
