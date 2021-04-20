# May 2021 Take Home!

## What it is...

1. Download the 2019 OLTP Adventure Works database (https://docs.microsoft.com/en-us/sql/samples/adventureworks-install-configure?view=sql-server-ver15&tabs=ssms) and restore on a local MSSQL instance by using SQL Server on Docker for Mac (https://docs.microsoft.com/en-us/sql/linux/quickstart-install-connect-docker?view=sql-server-ver15&pivots=cs1-bash)

2. Create a python application considering pep8 (https://www.python.org/dev/peps/pep-0008/) which does the following:
   1. Takes all rows from the Sales.CurrencyRate table from the restored database
   2. Sends an API request to https://free.currencyconverterapi.com/ in order to get the latest converstion rate
   3. Updates the database record w/ the latest conversion rate.
   4. Have the application "come alive" then "fall asleep" until the top of every hour so it gets the latest conversion rates

## Must Dos...

1. Use DocStrings
2. Save a requirement.txt file
3. Consider code complexity (i.e. O(n) complexity https://dzone.com/articles/learning-big-o-notation-with-on-complexity#:~:text=O(n)%20represents%20the%20complexity,after%20reading%20all%20n%20elements)
4. If O(n) complexity is optional, consider parallel processing through concurrent runs on a single thtread (i.e. multiprocessing) or multithreading! OR BOTH! :) -- multiprocess within each instantiated thread

## Don't forget -- send us your solution by the last day of May. We will then upload it to this repo so all people can see what people tried to solve the problem.
