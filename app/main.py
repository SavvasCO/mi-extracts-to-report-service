import database
import pickle
import sys
import lookForDuplicates
import combineExtracts
import os

command_name = sys.argv[1]

extracts_file = "unique-records.pkl"

if os.path.exists(extracts_file):
    all_records = pickle.load(open(extracts_file, "rb"))

if command_name == "combine-extracts":
    combineExtracts.combine_extracts()
    print("Saved all records in all-records.pkl")

if command_name == "look-for-duplicates":
    lookForDuplicates.look_for_duplicates(all_records)
    print("Saved all unique records in unique-records.pkl")

if command_name == "create-partitions":
    print("Creating partitions...")
    database.create_partitions_for_dates([record["last_updated"] for record in all_records])
    print("Created partitions")

if command_name == "add-records":
    print("Adding records...")
    database.insert_records(all_records)
    print("Added records.")
    database.close()