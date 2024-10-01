from datetime import datetime, timedelta
import psycopg2
import uuid
import json
import os

host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
database = os.getenv("DB_NAME")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")

connection = psycopg2.connect(
    host=host,
    port=port,
    database=database,
    user=user,
    password=password
)

cursor = connection.cursor()


def create_partitions_for_dates(dates):
    for date in dates:
        date_obj = datetime.strptime(date, "%d/%m/%Y %H:%M")
        date_for_partition_name = date_obj.strftime("%Y_%-m_%-d")
        date_for_range_from = date_obj.strftime("%Y-%m-%d")

        date_obj = date_obj + timedelta(days=1)
        date_for_range_to = date_obj.strftime("%Y-%m-%d")

        query = f"CREATE TABLE IF NOT EXISTS course_completion_events_{date_for_partition_name} PARTITION OF course_completion_events FOR VALUES FROM ('{date_for_range_from}') TO ('{date_for_range_to}');"
        cursor.execute(query)
        print(f"Added partition table course_completion_events_{date_for_partition_name}")

    connection.commit()

def insert_records(records):
    professions = json.load(open("professions.json"))["profession"]
    organisations = json.load(open("orgs.json"))["organisational_unit"]
    uid_grades = json.load(open("uid-grades.json"))["grades"]
    courses = json.load(open("courses.json"))["courses"]

    for index,record in enumerate(records):
        _=os.system("clear")
        print(f"{index+1} / {len(records)}")
        print(f"{str(int((index+1)/(len(records)) * 100))}% completed.")

        profession = next((r for r in professions if r["name"] == record["profession"]), None)
        organisation = next((o for o in organisations if o["id"] == int(record["organisationId"])), None)
        grade = next((grade for grade in uid_grades if grade["uid"] == record["user_id"]), None)
        course = next((course for course in courses if course["title"] == record["course_title"]), None)
        print(course)

        external_id = str(uuid.uuid4())
        user_id = record["user_id"]
        user_email = record["email"]
        course_id = "NULL_COURSE" if course == None else course["id"]
        course_title = record["course_title"]
        event_timestamp = datetime.strptime(record["last_updated"], "%d/%m/%Y %H:%M").strftime("%Y-%m-%d %H:%M")
        organisation_id = record["organisationId"]
        profession_id = None if profession == None else profession["id"]
        grade_id = None if grade == None else grade["grade_id"]
        grade_code = None if grade == None else grade["code"]
        profession_name = record["profession"]
        organisation_abbreviation = None if organisation == None else organisation["abbreviation"]

        insert_query = """
        INSERT INTO course_completion_events
        (external_id, user_id, user_email, course_id, course_title, event_timestamp, organisation_id, profession_id, grade_id, grade_code, profession_name, organisation_abbreviation)
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        values_to_insert = (external_id, user_id, user_email, course_id, course_title, event_timestamp, organisation_id, profession_id, grade_id, grade_code, profession_name, organisation_abbreviation)
        cursor.execute(insert_query, values_to_insert)    
    connection.commit()

def close():
    cursor.close()
    connection.close()
