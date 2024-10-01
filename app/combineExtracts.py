import csv
import os
import pickle

def combine_extracts():
    extracts_directory = "/extracts"

    all_records = []
    extract_file_names = os.listdir(extracts_directory)[0:2]
    print(extract_file_names)

    for file in extract_file_names:
        with open(f"{extracts_directory}/{file}") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                all_records.append(row)

        print(f"Records added from {file}")

    print(f"Successfully added {len(all_records)} records.")
    pickle.dump(all_records, open("all-records.pkl", "wb"))