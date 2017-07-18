#!/usr/bin/env python3

""" Code below runs three SQL queries on the database 'news':"""
# Database has three tables: authors, articles, and log

import psycopg2
import datetime


def db_connect():
    """ Creates and returns a connection to the database defined by DBNAME,
    as well as a cursor for the database.

    Returns:
        db, c - a tuple. The first element is a connection to the database.
                The second element is a ursor for the database.
    """
    try:
        db = psycopg2.connect("dbname=news")  # Connect to database
        c = db.cursor()  # Create cursor
        return db, c
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def execute_query(query):
    """Executes SQL Query.
        args: query is an SQL query passed as a String
        returns: A list of tuples containing query results.
    """
    db, c = db_connect()
    c.execute(query)
    return c.fetchall()


# Execute and return query 1:
def print_top_articles():
    """Prints out the top 3 articles based on page views."""
    print("Computing query 1...")
    query = (
        "SELECT articles.title, count(*) "
        "FROM articles JOIN log "
        "ON log.path = ('/article/' || articles.slug) "
        "GROUP BY articles.title "
        "ORDER BY count DESC "
        "LIMIT 3")
    ans = execute_query(query)
    print("Here are the three most popular articles in the database:")
    for title, count in ans:
        print(" > {} -- {} views".format(title, count))
    print("\n")


# Execute and return query 2:
def print_top_authors():
    """Prints the list of authors sorted by total page views"""
    print("Computing query 2...")
    query = (
        "SELECT authors.name, count(*) "
        "FROM authors JOIN articles ON authors.id = articles.author "
        "JOIN log ON log.path = ('/article/' || articles.slug) "
        "GROUP BY authors.name "
        "ORDER BY count DESC")
    ans = execute_query(query)
    print("Here are the authors sorted by total page views:")
    for author, count in ans:
        print(" > {} -- {} views".format(author, count))
    print("\n")


# Execute and return query 3:
def find_dates_errors_over_one():
    print("Computing query 3...")
    query = (
        "SELECT date, err_req * 100.0 / tot_req as err_pct "
        "FROM (SELECT date(time), count(*) as tot_req, "
        "SUM(CASE WHEN status != '200 OK' THEN 1 ELSE 0 END) as err_req "
        " FROM log GROUP BY date(time) ) as subq "
        "WHERE (err_req * 100.0 / tot_req) > 1.00")
    ans = execute_query(query)
    print("Dates with >1.0% error incidence:")
    for date, err_pct in ans:
        print(" > " + date.strftime("%B %d, %Y") + " -- " + "{0:.2f}".format(
              err_pct)+"% errors")


if __name__ == '__main__':
    print_top_articles()
    print_top_authors()
    find_dates_errors_over_one()
