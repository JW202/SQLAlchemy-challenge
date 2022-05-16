# SQLAlchemy-challenge

Part 1: Climate Analysis and Exploration
In this section, use Python and SQLAlchemy to perform basic climate analysis and data exploration of your climate database. Complete the following tasks by using SQLAlchemy ORM queries, Pandas, and Matplotlib.
1. Precipitation Analysis
    * Design a query to retrieve the last 12 months of precipitation data and load the query results into a Pandas DataFrame.
    * Use Pandas to print the summary statistics for the precipitation data.

2. Station Analysis
    * Design a query to calculate the total number of stations.
    * Design a query to find the most active stations.
    * List the stations and observation counts in descending order.
    * Design a query to retrieve the last 12 months of temperature observation data (tobs).
    * Filter by the station with the highest number of observations.
    * Plot the results as a histogram.

Part 2: Design Your Climate App
Now that I have completed my initial analysis, I can design a Flask API based on the queries that you have just developed.
    * route "/" 
    * precipitation
    * stations
    * tobs
    * start and start/end dates
