# Script to migrate MI extracts to the Reporting database

## Pre-run Preparation

### Import data

#### 1. Courses

Export courses `id` and `title` from the `learner_record.course_record` database. 

Save it as `courses.json` in the `app` directory. Make sure it looks like this:

```json
{
"courses": [
	{
		"id" : "ABC",
		"title" : "Course 1"
	},
	{
		"id" : "BCD",
		"title" : "Course 2"
	},
	{
		"id" : "DEF",
		"title" : "Course 3"
	}
...
```

#### 2. Organisations

Export organisations from the `csrs.organisational_unit` database into a file called `orgs.json`.

Make sure it looks like this:

```json
{
"organisational_unit": [
	{
		"id" : 1,
		"parent_id" : null,
		"code" : "123",
		"abbreviation" : "O1",
		"name" : "Org1",
		"payment_methods" : "PURCHASE_ORDER",
		"agency_token_id" : null,
		"created_timestamp" : "2000-10-01 00:00:00:00",
		"updated_timestamp" : "2000-10-01 00:00:00:00"
	},
	{
		"id" : 1,
		"parent_id" : null,
		"code" : "124",
		"abbreviation" : "O2",
		"name" : "Org2",
		"payment_methods" : "PURCHASE_ORDER",
		"agency_token_id" : null,
		"created_timestamp" : "2000-10-01 00:00:00:00",
		"updated_timestamp" : "2000-10-01 00:00:00:00"
	},
...
```
#### 3. Professions

Export professions from `csrs.profession` to `professions.json`. It should look like this:

```json
{
"profession": [
	{
		"id" : 1,
		"parent_id" : null,
		"name" : "Profession1"
	},
	{
		"id" : 2,
		"parent_id" : null,
		"name" : "Profession2"
	},
```

#### 4. User grades

Export grade ID and Code for users into a file `uid-grades.json`.

It should look like this:

```json
{
"grades": [
	{
		"id" : 1,
		"uid" : "abc",
		"grade_id" : 1,
		"code" : "GR1"
	},
	{
		"id" : 2,
		"uid" : "def",
		"grade_id" : 3,
		"code" : "GR3"
	},
```

## Running the scripts

### Combine extracts

```sh
python main.py combine-extracts
```

This scripts grabs all the extracts under a specified directory and combines them into a binary file called `all-records.pkl`. This file will be used in the other commands, so make sure you run this first.

### Look for duplicates

```sh
python main.py look-for-duplicates
```

This scripts gets the combined extracts file (`all-records.pkl`) and creates a new file called `unique-records.pkl` with duplicates removed.

### Create partitions

```sh
python main.py create-partitions
```

This script creates partitions for each day in the unique records file (`unique-records.pkl`).

### Add records

```sh
python main.py add-records
```

This scripts creates database records in the `course_completion_events` table in the specified Postgres database. This command will take a while, especially if there are many records in the `unique-records.pkl` file
