
import pyodbc
import ping3
import time


"""
Test connection to connect to a SQL database using pyodbc
"""

# Record the start time
start_time = time.time()

## start count and assign localhost 
count=1
state = False
localhost = '127.0.0.1'

# a list of drivers to test
drivers=[
    " ",
    "Driver={SQL Server};",
    "Driver={SQL Native Client};",
    "Driver={SQL Server Native Client 10.0};",
    "Driver={SQL Server Native Client 11.0};",
    "Driver={ODBC Driver 11 for SQL Server};",
    "Driver={ODBC Driver 13 for SQL Serve};",
    "Driver={ODBC Driver 17 for SQL Server};",
    "Driver={ODBC Driver 18 for SQL Serve};" 
   
]

# a list of server names to test
server_names=[
    "127.0.0.1",
    "localhost\SQLEXPRESS"
]

# other connection parameters
port_name="5000"  # port number
user_name="***********"  # database username
password="************"  # database password
db_name="*************"  # database name

print('################# Start ###################')

for driver in drivers:
    for server_name in server_names:
        # connection string
        connection_string=(
            f"{driver}"
            f"Server={server_name}, {port_name};"
            f"UID={user_name};"
            f"PWD={password};"
            f"Database={db_name}"
        )
    

        try:
            # Establish a database connection
            connection = pyodbc.connect(connection_string)

            # cursor object to interact with the database
            cursor = connection.cursor()

            # SQL query to retrieve table names
            query = "SELECT table_name = t.name FROM sys.tables t"
            table_query = "SELECT * from sys.column"

            # Execute the query
            cursor.execute(query)
            print('@@ ****** Connected Successfully ****** @@')
            print('_____________________________________________________________________')
            # Fetch and print the table names
            table_names = [row.table_name for row in cursor.fetchall()]
            column_names = [col.colname for col in cursor.fetchall()]
            print(f"Tables in the database on server '{server_name}' are listed below:")
            print('___________________________________________________________________')
            for table_name in table_names:
                print(table_name, end='   ***   ')
                
            print()
            # Loop through each table and retrieve its columns
            for table_name in table_names:
                print('____________________________________')
                print(f"Columns in the table '{table_name}':")
            
     
                # SQL query to retrieve column names for the current table
                column_query = f"SELECT column_name = c.name FROM sys.columns c WHERE c.object_id = OBJECT_ID('{table_name}')"
                
                
                # Execute the column query
                cursor.execute(column_query)
                
                # Fetch and print the column names for the current table
                column_names = [col.column_name for col in cursor.fetchall()]
                
                for column_name in column_names:
                    print(column_name)
                    
   
            print('_______________________________________________')
            
            state = True
            success = "@@@ At least one Successfull connection was acquired! @@@"

            # Close the cursor and connection
            cursor.close()
            connection.close()

        except pyodbc.Error as e:
            print(f"Error connecting to server '{server_name}' with driver '{driver}' ##Error is: {e}")
            failure = "!!! No connection  made !!!"
        except Exception as e:
            print(f"Error: {e}")
            failure = "!!! No connection made !!!"
        print('############# pinging server #################')
        # Ping the IP address
        response_time = ping3.ping(server_name) ##server_name

        if response_time is not None:
            print(f"Response time for {server_name}::: {response_time} ms")
        else:
            print(f"Failed to ping {server_name}")
        print('############# Round check #################')
        print('#############')
        print(f'Round {count} Executed')
        count += 1
        print('#############')
        print('############# going again #################')

print('################# Checking time ##################')
    
    
# Record the end time
end_time = time.time()

# Calculate the execution time
execution_time = end_time - start_time

print(f"Script execution time: {execution_time} seconds")
if state == True:
    print(success)
else:
    print(failure)
print('################### End ####################')

input("Press Enter key to exit")

