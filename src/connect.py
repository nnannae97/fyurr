import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2.extensions import connection
# database connection with postgres psycopg2 driver...
# --------------------------------------------
def data_conn() -> connection:
     """this function creates a local database connection and returns the connection object\n
          tis connection object can then be used to perform database operation.\n
          It does not take any params
     """
     while True:
          try:
               conn = psycopg2.connect(host='localhost',database='fyurr',
                                        user='postgres',password='king2002',cursor_factory=RealDictCursor)
               return conn
          except Exception as error:
               print("Connection to database failed")
               print(f"Error: {error}")

def main():
     try:
          conn = data_conn()
          cur = conn.cursor()
          print("added successfully")
          conn.commit()
          print("changes flushed to database")
     except Exception as err:
          # print(f"failed to add to db due to error: {err}")
          pass

if __name__ == '__main__':
     main()
