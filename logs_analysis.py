# Code below runs three SQL queries on the database 'news':
# Database has three tables: authors, articles, and log

import psycopg2
import datetime

db = psycopg2.connect("dbname=news")  # Connect to database
c = db.cursor()  # Create cursor


# Execute and return query 1:
print("Computing query 1...\n")
c.execute(
    "SELECT articles.title, count(*) "
    "FROM articles JOIN log "
    "ON log.path ILIKE ('%' || articles.slug) "
    "GROUP BY articles.title "
    "ORDER BY count DESC "
    "LIMIT 3")
ans1 = c.fetchall()
print("Here are the three most popular articles in the database:")
for title, count in ans1:
    print(" > " + title + " -- " + str(count) + " views")
print("\n")


# Execute and return query 2:
print("Computing query 2...\n")
c.execute(
    "SELECT authors.name, count(*) "
    "FROM authors JOIN articles ON authors.id = articles.author "
    "JOIN log ON log.path ILIKE ('%' || articles.slug) "
    "GROUP BY authors.name "
    "ORDER BY count DESC")
ans2 = c.fetchall()
print("Here are the authors sorted by total page views:")
for author, count in ans2:
    print(" > " + author + " -- " + str(count) + " views")
print("\n")


# Execute and return query 3:
print("Computing query 3...\n")
c.execute(
    "SELECT date, err_req * 100.0 / tot_req as err_pct "
    "FROM (SELECT date(time), count(*) as tot_req, "
    "SUM(CASE WHEN status != '200 OK' THEN 1 ELSE 0 END) as err_req "
    " FROM log GROUP BY date(time) ) as subq "
    "WHERE (err_req * 100.0 / tot_req) > 1.00")
ans3 = c.fetchall()
print("Dates with >1.0% error incidence:")
for date, err_pct in ans3:
    print(" > " + date.strftime("%B %d, %Y") + " -- " + "{0:.2f}".format(
          err_pct)+"% errors")

db.close()
