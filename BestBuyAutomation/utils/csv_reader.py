import csv
import os


class CSVReader:

    @staticmethod
    def read_csv(file_name):

        data = []

        base_dir = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )

        file_path = os.path.join(base_dir, "data", file_name)

        with open(file_path, newline='', encoding='utf-8') as csvfile:

            reader = csv.DictReader(csvfile)

            for row in reader:
                data.append(row)

        return data