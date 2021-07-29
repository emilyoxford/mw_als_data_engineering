##### Importing packages #####

import datetime
import numpy as np
import pandas as pd



##### Loading in data #####

cons_info = pd.read_csv('https://als-hiring.s3.amazonaws.com/fake_data/2020-07-01_17%3A11%3A00/cons.csv')
cons_email = pd.read_csv('https://als-hiring.s3.amazonaws.com/fake_data/2020-07-01_17%3A11%3A00/cons_email.csv')
cons_ecs = pd.read_csv('https://als-hiring.s3.amazonaws.com/fake_data/2020-07-01_17%3A11%3A00/cons_email_chapter_subscription.csv')



##### Creating "people" file #####

### Step 1: Join data

# left merge preserves all relevant constituent-level available and leaves missing information as NaN
merge_1 = cons_email[cons_email.is_primary == 1][['cons_id', 'email', 'cons_email_id']].merge(
    cons_info[['cons_id', 'create_dt', 'modified_dt', 'source']], on = 'cons_id', how = 'right'
)

# "We only care about subscription statuses where chapter_id is 1."
# again, left merge preserves all relevant constituent-level available and leaves missing information as NaN
merge_2 = merge_1.merge(
    cons_ecs[cons_ecs.chapter_id == 1][['cons_email_id', 'isunsub']], on = 'cons_email_id', how = 'left'
) 


### Step 2: Create "people" dataframe

people = merge_2.drop(columns = ['cons_email_id', 'cons_id']) # removing merge fields


### Step 3: substitute isunsub NaN's with 1

# referenced https://stackoverflow.com/questions/944700/how-can-i-check-for-nan-values for np.isnan() function
people.isunsub = people.isunsub.apply(lambda x: 1 if np.isnan(x) else x)


### Step 4: transform to correct data types

# boolean should be int, less confusing this way
people.isunsub = people.isunsub.astype(int) 

# change *_dt fields to actual pandas datetime format
people.create_dt = people.create_dt.apply(lambda x: pd.to_datetime(x.split(',')[1]))
people.modified_dt = people.modified_dt.apply(lambda x: pd.to_datetime(x.split(',')[1]))


### Step 5: format dataframe correctly

# putting columns in correct order
people = people[['email', 'source', 'isunsub', 'create_dt', 'modified_dt']]
# renaming columns to correct names
people = people.rename(columns = {
    'source': 'code', 'isunsub': 'is_unsub', 'modified_dt': 'updated_dt'
})


# Step 6: Export to CSV
people.to_csv('people.csv', index = False)



##### Creating "acquistion_facts" file #####

### Step 1: Extract revelent information from "people" dataframe
acq_facts = people[['email', 'create_dt']]


### Step 2: Create acquisition_date and transform to date
acq_facts['acquisition_date'] = acq_facts.create_dt.dt.date
# this column is no longer needed
acq_facts = acq_facts.drop(columns = 'create_dt')


### Step 3: Transform acq_facts into date and count of acquisitions on date
acq_facts = pd.DataFrame(acq_facts.acquisition_date.value_counts().reset_index().rename(
    columns = {'acquisition_date': 'acquisitions', 'index': 'acquisition_date'}
))
acq_facts.sort_values('acquisition_date', inplace = True)


### Step 4: Write acq_facts to CSV
acq_facts.to_csv('acquisition_facts.csv', index = False)