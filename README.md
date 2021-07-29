# MissionWired/ALS Data Engineering Exercise

## Description
This repository was created for a hiring exercise for MissionWired in summer 2021. In this exercise, data from three separate CSV files on constituent information ([Constituent Information](https://als-hiring.s3.amazonaws.com/fake_data/2020-07-01_17%3A11%3A00/cons.csv), [Constituent Email Addresses](https://als-hiring.s3.amazonaws.com/fake_data/2020-07-01_17%3A11%3A00/cons_email.csv), and [Constituent Subscription Status](https://als-hiring.s3.amazonaws.com/fake_data/2020-07-01_17%3A11%3A00/cons_email_chapter_subscription.csv)) are combined to generate two separate files: [people.csv](https://github.com/emilyoxford/mw_als_data_engineering/blob/main/people.csv) and [acquisition_facts.csv](https://github.com/emilyoxford/mw_als_data_engineering/blob/main/acquisition_facts.csv).


See the [original description of the exercise](#original-description-of-exercise) below for the full instructions.

## Files
This repository contains:
- 2 executable files:
    - [als_data_engineering.ipynb](https://github.com/emilyoxford/mw_als_data_engineering/blob/main/als_data_engineering.ipynb)
    - [als_data_engineering.py](https://github.com/emilyoxford/mw_als_data_engineering/blob/main/als_data_engineering.py)

- 2 output files:
    - [people.csv]()
        - Fields:
            - email (str): Primary email address
            - code (str): Source code
            - is_unsub (int): Boolean of whether the email address is subscribed to chap_1. 1 = unsubscribed, 0 = subscribed
            - created_dt (datetime): Person creation datetime
            - updated_dt (datetime): Person updated datetime
    - [acquisition_facts.csv](https://github.com/emilyoxford/mw_als_data_engineering/blob/main/acquisition_facts.csv)
        - Fields:
            - acquisition_date (date): Calendar date of acquisition
            - acquisitions (int): Number of constituents acquired on acquisition_date

## How to run
To generate [people.csv](https://github.com/emilyoxford/mw_als_data_engineering/blob/main/people.csv) and [acquisition_facts.csv](https://github.com/emilyoxford/mw_als_data_engineering/blob/main/acquisition_facts.csv), there are two options:
1. Open [als_data_engineering.ipynb](https://github.com/emilyoxford/mw_als_data_engineering/blob/main/als_data_engineering.ipynb). Run all cells in order.
- This option is intended for those who wish to understand the process by which the files were created. There are more comprehensive comments on what is being done (and why) at each step, with examples of how the data looks at each step of transformation.

2. From the command line, run "python3 als_data_engineering.py"
- This option is intended for those who want to generate people.csv and acquisition_facts.csv quickly and do not need a more detailed explanation of how the code is intended to work.

## Software used
The code in this repository was written using [Python 3.7.7](https://www.python.org/downloads/release/python-377/). Both the .py and the .ipynb files require the following Python libraries to be installed:
- [numpy](https://numpy.org/install/) (version used in this repository: 1.19.2)
- [pandas](https://pandas.pydata.org/docs/getting_started/install.html) (version used in this repository: 1.19.2)

Note that earlier/later versions of Python and these libraries may result in incompatibilities while running the code. If the code breaks, try running with the versions used above.

## Other notes

### Why custom functions were not written

While I considered breaking each step of the code into separate functions, I ultimately chose to write code without creating any new functions, because:
- the code is meant for this exercise alone
- the size of the data and the complexity of the operations do not necessitate parallel processing or other tools that would likely require custom functions
- writing the code in a linear, step-by-step format may improve readability for a task of this (relative) simplicity

If this process needed to be used multiple times on multiple files regularly, I would have chosen to use custom Python classes and functions as needed to ensure standardized output files each time.

### Interpretation of "updated_dt" field

The instructions for the "updated_dt" field in [people.csv](https://github.com/emilyoxford/mw_als_data_engineering/blob/main/people.csv) were initially unclear to me, as each of the three original CSVs have what I assume is the equivalent field ("modified_dt"), and the "modified_dt" field was different for each instance of constituent, email address, and subscruption in the CSVs.

I ultimately decided to use the "modified_dt" field from the Constituent Information CSV because it appeared to represent instances of a single constituent's _personal_ information being updated. This interpretation aligned with what I believe was the intention of the "create_dt" field: the datetime that one individual's _personal_ information was added to the dataset.


## Original description of exercise

### ALS Hiring
#### Data Engineer Exercise

The purpose of this exercise is to evaluate your level of skill when it comes to manipulating and aggregating a large dataset through code. We’ll evaluate the quality, output and readability of your code as well as the efficacy of provided documentation.
We recommend using Python and Pandas to complete this exercise, although you can use whatever language you like (e.g. R or SQL). Most of our production data engineering work is done using Python, Pandas and PySpark (a "big data" alternative to Pandas).

We recommend submitting your code by way of a personal GitHub repository. Directly submitting code files is also acceptable.

Draft documentation describing how a reviewer can run your app locally. Be sure to include steps like installing dependencies or other “pre-flight” configurations necessary for your code to run.

##### Dataset
A dataset simulating CRM data is available in some public AWS S3 files:
- Constituent Information: https://als-hiring.s3.amazonaws.com/fake_data/2020-07-01_17%3A11%3A00/cons.csv
- Constituent Email Addresses: https://als-hiring.s3.amazonaws.com/fake_data/2020-07-01_17%3A11%3A00/cons_email.csv
    - Boolean columns (including is_primary) in all of these datasets are 1/0 numeric values. 1 means True, 0 means False.
- Constituent Subscription Status: https://als-hiring.s3.amazonaws.com/fake_data/2020-07-01_17%3A11%3A00/cons_email_chapter_subscription.csv
    - We only care about subscription statuses where chapter_id is 1.
    - If an email is not present in this table, it is assumed to still be subscribed where chapter_id is 1.
    
Use these files to complete the exercises below.
 
##### Exercises
1. Produce a “people” file with the following schema. Save it as a CSV with a header line to the working directory.

|Column|Type|Description|
|---|---|---|
|email|string|Primary email address|
|code|string|Source code|
|is_unsub|boolean|Is the primary email address unsubscribed?|
|created_dt|datetime|Person creation datetime|
|updated_dt|datetime|Person updated datetime|

2. Use the output of #1 to produce an “acquisition_facts” file with the following schema that aggregates stats about when people in the dataset were acquired. Save it to the working directory.

|Column|Type|Description|
|---|---|---|
|acquisition_date|date|Calendar date of acquisition|
|acquisitions|int|Number of constituents acquired on acquisition_date|
