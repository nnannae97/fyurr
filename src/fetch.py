# TODO: implement logic for venue detail fetching and display to frontend.

from psycopg2.extensions import connection
from psycopg2.extras import RealDictRow
from .connect import data_conn
from typing import Any

def fetch_city(con: connection):
     """fetches list of all the cities in the database return a query set and list of all cities
          to fetch the venues for
     """
     query = """select city, state from venue"""
     try:
          csx = con.cursor()
          csx.execute(query)
          result: list = csx.fetchall()
          # if result:
          #      for i in result:
          #           i.setdefault('venues', [])
          return result

     except Exception as err:
          print(err)

def fetch_venue_list(city):
     """
     fetches list of venue and formats in correct order
     """
     query = """select venue.id,name,count(show.*) as num_upcoming_shows
                    from venue,show where city = %s and venue.id = show.venue_id group by venue.id;"""
     try:
          conn = data_conn()
          csx = conn.cursor()
          csx.execute(query,(city,))
          l = csx.fetchmany()
          return l
     except Exception as err:
          print(err)

def get_list():
     """this util function fetches the cities and checks for the listed venues and fetches them based\n
          on city name,then it sets a key of venues for each item and gives it a value returned from\n
          the fetch_venue_list function.
     """
     ct = data_conn()
     data_list: list[RealDictRow] = fetch_city(ct)
     print(data_list)
     if data_list:
          for item in data_list:
               city = item.get('city')
               ven = fetch_venue_list(city)
               item.setdefault('venues',ven)
     ct.close()
     return data_list
# ------------------------------------------------------------------------------------------------
# ================================================================================================
# NOTE: venue detail implementation.

def get_shows(venue_id):
     """this function takes in the venue id and fetches list of upcoming shows"""
     try: 
          query = """select artist.id as artist_id,artist.name as artist_name,
                    artist.image_link as artist_image_link,show.start_time as start_time from artist,venue,show
                    where venue.id = show.venue_id and show.artist_id = artist.id and venue.id = %s"""
          con = data_conn()
          csx = con.cursor()
          csx.execute(query,(venue_id,))
          res = csx.fetchmany()
          return res
     except Exception as err:
          print(err)
     

def get_venue_detail(id):
     """this gets the detailed information about a venue,it handles the implementation of fetching
          a specific venue and also the list of shows related to it.
          """
     try:
          query = """select * from venue where id = %s"""
          con = data_conn()
          csx = con.cursor()
          csx.execute(query,(id,))
          v: RealDictRow = csx.fetchone()
          if v:
               shows = get_shows(id)
               date_to_string(shows)
               v.setdefault('past_shows',[])
               if shows:
                    v.setdefault('upcoming_shows',shows)
                    # set the upcoming shows key to the val gotten from get_shows().
                    v.setdefault('upcoming_shows_count',len(shows))
               else:
                    v.setdefault('upcoming_shows',[])
                    v.setdefault('upcoming_shows_count',0)

          return v
     except Exception as err:
          print(err)

def date_to_string(u_shows):
     for i in u_shows:
          d = i.pop('start_time')
          i.setdefault('start_time',str(d))
                              
if __name__ == '__main__':
     pass
     # d = get_venue_detail(1)
     # print(d)


