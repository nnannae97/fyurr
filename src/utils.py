# =======================================

""" A util mode to handle some useful data processing from request objects"""
# function to process dict from request...
# _______________________________________
from typing import Any
from psycopg2.extensions import connection
from werkzeug.datastructures import ImmutableMultiDict

from src.connect import data_conn
from .sql import sql_statement

def process_dict(data: ImmutableMultiDict ) -> tuple[dict,list | None]:
     """this function iterates through the data and creates a primitive dict object with the key
          with the keys and values already existing...
          it returns a dictionary and list, so prepare to receive two valus of different values.
          note: if u store it in one variable,it is converted to a tuple containing a dictionary\n
          and list.
     """
     genres: list | None = data.getlist('genres')
     # first get the list of genres...
     proc_data = {}
     for key,value in data.items():
          if key != 'genres':
               if key == 'seeking_talent' or key == 'seeking_venue':
                    if value == 'y':
                         proc_data.setdefault(key,'True')
                    else:
                         proc_data.setdefault(key,'False')
               proc_data.setdefault(key,value)
     return proc_data,genres
     # returns two values which by default becomes a tuple of values...


def dict_to_tuple(data: dict,flag=None) -> tuple:
     """util function to convert dict to tuple \n
     it has a branching that checks for the presence of seeking venue for artists if flag is A
     if it isnt avaliable,it gives a default of false so as to sync the tuple.
     if flag is V, it branches branches and does same thing, but it does it for seeking talent.
     """
     # dic = {"name":"John Doe","age":"30","Job":"Software Developer","nationality":"American"}
     list_data: list = []
     for key,value in data.items():
          list_data.append(value)

     if flag == 'A':
          venue = data.get("seeking_venue")
          # i ran into an issue where if the seeking talent was not provided in the frontend,
          # the program crashed because the tuple passed into the insert to cursor.execute() function
          # was out of range with the no of variables in the prep statement (%s)
          if venue is None:
               """ this branching checks for the presence of seeking venue for artists\n
                    if it isnt avaliable,it gives a default of true so as to sync the tuple.
               """
               desc = list_data.pop()
               list_data.append("False")
               list_data.append(desc)
     elif flag == 'V':
          """ if flag is V branches and does same thing, but it does it for seeking talent."""
          talent = data.get("seeking_talent")
          if talent is None:
               """ this branching checks for the presence of seeking venue for artists\n
                    if it isnt avaliable,it gives a default of true so as to sync the tuple.
               """
               desc = list_data.pop()
               list_data.append("False")
               list_data.append(desc)

     proc_tuple = tuple(list_data)
     # print(f'type of proc data: {type(proc_tuple)}')
     # print(proc_tuple)
     return proc_tuple
     
#-------------------------------------------------------------------------------------------------                 
def insert_into_db(conn: connection,data: dict,flag='A') -> bool | None:
     """This function would be used to insert the request form data into db\n
          like this...
          data = process_dict(request.form)\n
          conn = data_conn() #from connect.py\n
          insert = insert_into_db(conn,data,flag='A')\n
          It takes in the connection as param as well as the proccesed primitive dictionary data\n
          and also the flag to indicate type of submission.\n
          1. use 'A' flag if it is an artist submission \n
          2. user 'V' flag for Venue submission \n
          3. user 'SH' flag for show submmission \n
     """
     # pass the database connection as param along side the data in dict form
     # process dict obj to tuple
     try:
          cursor = conn.cursor()
          if flag=='A':
               prep_data = dict_to_tuple(data, flag='A')
               sql = sql_statement(flag)
               cursor.execute(sql,prep_data)
               # handles branching for when flag is A, which means its an add artiste command.
          elif flag == 'V':
               prep_data = dict_to_tuple(data,flag='V')
               sql = sql_statement(flag='V')
               cursor.execute(sql,prep_data)
               # handles branching for venue insert, it prepares the appropriate sql based on flag.
          elif flag == 'SH':
               prep_data = dict_to_tuple(data)
               sql = sql_statement(flag='SH')
               cursor.execute(sql,prep_data)
          conn.commit()
          return True
     except Exception as err:
          print(f"adding to db failed\n***************\n{err}")
     
     # print(f"data\n{} \n successfully added to db")
def get_id(dictionary: dict):
     """small util function to get an id when name is passed as a param"""
     try:
          con = data_conn()
          ctx = con.cursor()
          name = dictionary.get('name')
          if name:
               ctx.execute("""select id from artist where name = %s""",(name,))
               d = ctx.fetchone()
               id = d.get('id')
               return id

     except Exception as err:
          print(err)



def genre_submission(genres: list,id,conn: connection):
     """this function takes in a list of genres and id and the connection object"""
     try:
          ctx = conn.cursor()
          query = """select id from genre where name = %s"""
          ids = []
          for i in genres:
               ctx.execute(query,(i,))
               d = ctx.fetchone()
               ids.append(d.get('id'))

          query_i = """insert into artist_genre values (%s, %s)"""
          for i in ids:
               ctx.execute(query_i,(flag,id,i))
          # looped through the list of ids and added the artist id and each item id into the 
          # linking table.
          conn.commit()
          return True
     except Exception as err:
          print(f'\n**************\nfailed with {err}')

def v_genre_submission(genres: list,id,conn: connection):
     """does same as genre_submission but for venues"""
     try:
          ctx = conn.cursor()
          query = """select id from genre where name = %s"""
          ids = []
          for i in genres:
               ctx.execute(query,(i,))
               d = ctx.fetchone()
               ids.append(d.get('id'))

          query_i = """insert into venue_genre values (%s, %s)"""
          for i in ids:
               ctx.execute(query_i,(id,i))
          # looped through the list of ids and added the artist id and each item id into the 
          # linking table.
          conn.commit()
          return True
     except Exception as err:
          print(f'\n**************\nfailed with {err}')






if __name__ == '__main__':
     pass
     # dict_to_list()