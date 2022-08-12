from psycopg2.extensions import connection
from .connect import data_conn
from .sql import sql_statement,query_statement
"""
This module contains classes to handle to formatting a encapsulation of data gotten from db
"""
# TODO handle logic for building show data with static methods.
# TODO group instances of show data in a list and return to code...
class ShowData:

     def __init__(self,id,venue_id,venue_name,artist_id,artist_name,
                    artist_image_link,start_time) -> None:
          self.id = id
          self.venue_id: str  = venue_id
          self.venue_name: str = venue_name
          self.artist_id: str = artist_id
          self.artist_name: str = artist_name
          self.artist_image_link: str = artist_image_link
          self.start_time: str = start_time

     def get_dict(self,flag: str | None = None) -> dict:
          """converts the properties of the object to a dictionary\n

               makes use of flag to get present the data in the best suited format.\n
               user:
               get_dict(flag='L') # for list presentation
          """
          # NOTE, I added str() to self.start_time to convert it to a string object
          data = {
               "venue_id": self.venue_id,
               "venue_name": self.venue_name,
               "artist_id": self.artist_id,
               "artist_name": self.artist_name,
               "artist_image_link": self.artist_image_link,
               "start_time": str(self.start_time)
          }
          return data        

     @classmethod
     def create_object(cls,**kwargs):
          return cls(**kwargs)

     def __str__(self) -> str:
          s = self.get_dict()
          return f'{s}'
          
     def __repr__(self) -> str:
          d = self.get_dict()
          return f'{d}'
          


class ShowHandler:
     """Handles operation for fetching formatting and representing show data"""
     
     def __init__(self) -> None:
          self.shows: list = []


     def get_convert_data(self) -> list:
          """gets the list data of dictionaries to be displayed to the frontend"""
          data = []
          # loop through the shows attribute and return a list of dictionaries
          for i in self.shows:
               d = i.get_dict()
               data.append(d)
          return data


     @staticmethod
     def fetch_shows(conn: connection):
          """pass in the connection object and let the function perform its magic."""
          query = sql_statement(flag='SH_ALL')
          try:
               cursor = conn.cursor()
               cursor.execute(query)
               shows = cursor.fetchall()
               l =  ShowHandler._process_list(shows)
               return l
          except Exception as err:
               print(f"an error occurred: \n****************\n{err}")

     @staticmethod
     def _process_list(data: list | tuple| None):
          """iterates through a list of RealDictRow object and returns a \n
          primitive list of dictionary"""
          l: list = []
          if data is not None:
               for i in data:
                    d = {}
                    for k,v in i.items():
                         d.setdefault(k,v)
                    l.append(d)
               return l

     @staticmethod
     def _proc_dict(data) -> dict | None:
          """formats realdictrow objects to native python dictionaries"""
          if data:
               d: dict = {}
               for k,v in data.items():
                    d.setdefault(k,v)
               # return the dictionary after the operation.
               return d



     @staticmethod
     def search_artist(conn: connection,d: dict) -> dict |  None:
          """takes in the conn and dictionary object as arguments, it searches the db for\n
               the artist with the specified id and returns the result
          """
          id = d.get("artist_id")
          if id:
               try:
                    query =  query_statement(flag='QA')
                    cur = conn.cursor()
                    cur.execute(query,(id,))
                    data = cur.fetchone()
                    # close the connection and return the data
                    dt = ShowHandler._proc_dict(data)
                    if dt:
                         return dt
               except Exception as err:
                    print(f'operation failed with err: {err}\n')
          return None
     @staticmethod
     def search_venue(conn: connection, d: dict):
          """searches the database with id from the dict passed as an argument to the method"""
          # get cursor
          id = d.get('venue_id')
          try:
               cursor = conn.cursor()
               cursor.execute("""select name from venue where id = %s""",(id,))
               queryset = cursor.fetchone()
               qs = ShowHandler._proc_dict(queryset)
               del queryset
               return qs
          except Exception as err:
               print(f'failed with error {err}')
     
     @staticmethod
     def combine_result(show_data:dict, artist_data: dict,venue_data: dict) -> dict | None:
          """combines the results from the two querysets,the show data and combines them into one dictionary\n
               and return the dictionary. It takes three arguments as params.
               the show data, the artist data, and venue data.
          """
           # iterate through dictionary
          try:
               d: dict = {}
               for c,i in venue_data.items():
                    d.setdefault(f'venue_{c}',i)
               # loop through the venue data
               # then loop through the artist data
               for k,v in artist_data.items():
                    d.setdefault(f'artist_{k}', v)               
               data = show_data | d
               return data
              
          except Exception as err:
               print(f'Exceptio: {err}')


     @staticmethod
     def build_show(conn: connection,raw_data):
          """takes in one raw show data, performs the neccesary search queries formats and then\n
               builds a nicely formatted object from it.
          """
          try:
               artist = ShowHandler.search_artist(conn,raw_data)
               venue = ShowHandler.search_venue(conn,raw_data)
               if artist and venue:
                    result_dic = ShowHandler.combine_result(raw_data,artist,venue)
                    if result_dic:
                         obj = ShowData.create_object(**result_dic)
                         return obj
                    
               raise Exception("Artist and venue do not exist")
          except Exception as err:
               print(err)

          # 
          pass


     @classmethod
     def build_list(cls):
          """This is the entry point for building this object,it doesnt take anu arguments,\n
               it encapsulates all the other staticmethods and returns an instance of ShowHandler\n
               which contains a list property that is a list of all individual ShowData objects.
          """
          obj = cls()
          conn = data_conn()
          data = ShowHandler.fetch_shows(conn)
          # obj_list = []
          if data:
               for i in data:
                    s_obj = ShowHandler.build_show(conn,i)
                    obj.shows.append(s_obj)
               return obj



if __name__ == '__main__':
    pass