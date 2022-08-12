# TODO: Handle logic for fetching artists.
# TODO TODO; find out why the query doesnt return a value for indexes apart form 3,4,6
from .connect import data_conn
from psycopg2.extras import RealDictRow
from .fetch import date_to_string

def get_artist_list():
     """this function handles logic for fetching the list of artists."""
     try:
          query = """select id,name from artist"""
          con = data_conn()
          csx = con.cursor()
          csx.execute(query)
          a_list = csx.fetchall()
          # print(a_list)
          con.close()
          return a_list
     except Exception as err:
          print(err)

def get_shows(id):
     """this function fetches the shows related to an artist"""
     try:
          query = """select venue.id as venue_id, 
               venue.name as venue_name,venue.image_link as venue_image_link,
               show.start_time as start_time from artist,show,venue where artist.id = show.artist_id 
               and show.venue_id = venue.id and artist.id = %s"""
          con = data_conn()
          csx = con.cursor()
          csx.execute(query,(id,))
          res = csx.fetchmany()
          date_to_string(res)
          # print(res)
          return res
     except Exception as err:
          print(err)


def get_artist_detail(artist_id):
     """this function gets the detailed information about an artist,including the upcoming shows,
          associated with it.\n
          it returns the artist details along with the shows related to it.\
     """
     try:
          query = """select artist.* from artist where artist.id = %s"""
          con = data_conn()
          csx = con.cursor()
          csx.execute(query,(artist_id,))
          a_data: RealDictRow =  csx.fetchone()
          a_data.setdefault('past_shows',[])
          a_data.setdefault('past_shows_count',0)
          # set default show counts as an empty list and 0.
          shows = get_shows(artist_id)
          # get shows related to the artist.
          if shows:
               a_data.setdefault('upcoming_shows',shows)
               a_data.setdefault('num_upcoming_shows',len(shows))
          return a_data
     except Exception as err:
          print(err)

def main():
     d = get_artist_detail(11)
     print(d)
     # get_shows(4)


if __name__ == '__main__':
     main()