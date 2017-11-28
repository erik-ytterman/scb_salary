import pandas as pd

import scb_interfaces as scbi

# Utility function to match key tuples in record
def matcher_generator(pattern):
    def matcher(record):
        key, value = record
        states = [ p == None or k == p for k, p in zip(key, pattern) ]
        # print(key, pattern, states)
        return all(states)
    return matcher

# Load regions with records of type "(('0319',), ('Älvkarleby',))"
source = open('./kommunlankod.csv')        
regions = [ record for record in scbi.parse_regions(source) ]

# Filter salaries to get records with key "('0180', 2, 20, 2015)"
keypattern = ('0180',)
matcher = matcher_generator(keypattern)
regionset = filter(matcher, regions)

# Load salaries with records of type "(('0180', 2, 20, 2015), (109.4, 106.2))"
salaries = [ record for record in scbi.get_salaries() ]

# Filter salaries to get records with key "('0180', 2, 20, 2015)"
keypattern = ('0180', None, None, 2015)
matcher = matcher_generator(keypattern)
salaryset = filter(matcher, salaries)

# Utiliy to get Pandas dataframe
def get_dataframe():
    cols = ['gender', 'age', 'average', 'median', 'count']
    
    def g(salaryset):
        for key, value in salaryset:
            kid, gender, age, year = key
            average, median, count = value
            yield([gender, age, average, median, count])

    rows = [ datum for datum in g(salaryset) ]

    return pd.DataFrame(rows, columns=cols)
