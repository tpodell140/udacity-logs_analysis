# Logs Analysis Project Submission

## Project Description
This project uses a Python3 file to run three queries on a database for a news website. 

The database contains three tables (author, articles, and log) and is a model of page views on a news website. This database is intended to be used for website analytics.

The three queries answer the following:
1. What are the three most popular articles in the database, based on page views?
2. What are the three most popular authors, based on total page views for all articles?
3. On which days did more than 1.0% of page view requests result in an error?

## Setting up the database
The `news` database used in this project is contained in the file  `newsdata.sql`, [which is available in the zip file linked here.](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)

Once you have downloaded and extracted the `newsdata.sql` file, initialize and connect to the database. This can be done with the following command using PostgreSQL:
```
psql -d news -f newsdata.sql
```


## Running the Code
Execute the `logs_analysis.py` file in a Terminal:

```
python3 logs_analysis.py
```
