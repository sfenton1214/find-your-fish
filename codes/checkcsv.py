# The purpose of this program is to check to make sure the csv is properly put together
# i.e. all fish are pointed to by some question, and every question points to something
import csv
from sys import argv

# Save the user input
user = argv[1]

# Error check for argument number, provide correct usage
if len(argv) != 2:
    print("Usage: python checkcsv.py [name of your csv].csv")
    exit(1)

# Open the csv, user must input csv name
with open(user, "r") as f:
    reader = csv.DictReader(f)
    rows = list(reader)

# Create a tracker of how many errors were found
errors = 0

# Make sure all questions lead to two places
for row in rows:
    if (row['a'] and not row['b']) or (row['b'] and not row['a']):
        # Tell the user what row has a flaw, that way they can revise the csv
        print("The question with id " + row['id'] + " does not point anywhere.")
        errors += 1

# Create a list that contains all the places that questions lead
dest = []
for row in rows:
    if row['a'] and row['b']:
        dest.extend((row['a'], row['b']))

# Create a list of all ids
ids = []
for row in rows:
    ids.append(row['id'])

# Go through the fish and make sure something points to them
for row in rows:
    # If the row represents a fish
    if not row['a'] and not row['b']:
        # Make sure its id is in the list of destinations
        if row['id'] not in dest:
            # Tell the user what row has a flaw, that way they can revise the csv
            print("The fish in row " + row['id'] + " is not pointed to by anything")
            errors += 1

# Make sure that nothing in the csv points further than the final id
for row in rows:
    # If it's a question
    if row['a'] and row['b']:
        # See if it points somewhere
        if row['a'] not in ids or row['b'] not in ids:
            print("The question with id " + row['id'] + " does not point to an existing row.")
            errors += 1

print("There are " + str(errors) + " errors.")