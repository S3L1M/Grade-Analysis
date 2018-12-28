# Imports
import pandas as pd
from numpy import NaN

# Definitions
d = pd.read_excel('Grades.xlsx')
SUB_COLS = ['Sub'+str(i) for i in range (1, 8)]     #Subject column names [Sub1, Sub2, ...]
GRADE_COLS = ['Grade'+str(i) for i in range (1, 8)] #Subject column names [Grade1, Grade2, ...]

subs = set()    # set of all subjects name
for col in SUB_COLS:
    subs |= set(d[col].dropna().unique())

dataset = {k:[] for k in {'ID' ,'Name', 'Level'}|subs}    # Initialize Data Dictionary

for i, r in d.iterrows():
    # Add ID, Name, Level to dataset arrays
    dataset['ID'].append(r['ID'])
    dataset['Name'].append(r['Name'])
    dataset['Level'].append(r['Level'])

    # Assume all grades are NaN
    for s in subs: dataset[s].append(NaN)

    # Assign each grade to its corrosponding key subject in dataset
    for col in SUB_COLS:
        if r[col] in subs:
            dataset[r[col]][i] = int(r[GRADE_COLS[SUB_COLS.index(col)]])

df = pd.DataFrame(dataset)  # Create a clean DataFrame
df.to_pickle('dataset')     # Save clean data in pickle file
