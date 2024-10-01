import pickle

def look_for_duplicates(records):

    keys = []
    unique_records = []
    duplicates = []

    for record in records:
        composite_key = record["user_id"] + "///" + record["course_title"]
        if composite_key in keys:
            duplicates.append(composite_key)
            print(f"Found duplicate: {composite_key}")
        else:
            unique_records.append(record)
            
        keys.append(composite_key)

    print(f"Found a total of {len(duplicates)} duplicates.")
    open("duplicates.txt", "w").write("\n".join(duplicates))
    pickle.dump(unique_records, open("unique-records.pkl", "wb"))