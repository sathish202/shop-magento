import mysql.connector

def db_connect(host,user, psswd,):
    try:
        connection = mysql.connector.connect(host = host, user = user, psswd = psswd)
        if connection.is_connected():
            print("Your are now connected to MySql server")
            cursor = connection.cursor()
            database_name = input("Enter the database name: ")
            create_db_query = f"CREATE DATABASE {database_name}"
            cursor.execute(create_db_query)
            print(f"Database '{database_name}' created sucessfully")
            cursor.close()
            connection.close()
            print("MySql server conncetion is close")
    except mysql.connector.Error as error:
        print('Error', error)
db_connect(host=input("Enter the host name: "), user=input("Enter the user name: "), psswd=input("Enter the password: "))
