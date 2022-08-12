"""module for managing sql statements"""


INSERT_ARTIST = """insert into artist
                         (name,city,state,phone,image_link,facebook_link,website_link,
                         seeking_venue,seeking_description) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"""


SELECT_ALL_FROM_ARTIST = """select * from artist"""
SELECT_FROM_ARTIST = """select * from artist where %s = %s"""
SELECT_QUERY_ARTIST = """select name, image_link from artist where id = %s"""
# -------------------------------------------------------------------------------------------
INSERT_VENUE = """insert into venue
                         (name,city,state,address,phone,image_link,facebook_link,website_link,
                         seeking_talent,seeking_description) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

SELECT_ALL_FROM_VENUE = """select * from venue"""

# -----------------------------------------------------------------------------------------------
INSERT_SHOW = """insert into show (artist_id,venue_id,start_time) values (%s,%s,%s)"""
SELECT_ALL_FROM_SHOW = """select * from show"""
DEFAULT = """select * """


def sql_statement(flag: str ) -> str:
     """This function returns sql statements based on the flag passed into it..
          1. A flag for insert into artist query\n
          2. V for insert into venue query\n
          3.  SH for insert into show query\n
          4. SH_ALL flag for select all from show query\n
     """
     if flag == 'A':
          # return the insert artist statement if flag is A
          return INSERT_ARTIST
     elif flag == 'SA':
          return SELECT_ALL_FROM_ARTIST

     elif flag == 'V':
          return INSERT_VENUE
     elif flag == 'SH':
          return INSERT_SHOW
     elif flag == 'SH_ALL':
          return SELECT_ALL_FROM_SHOW
     else:
          return DEFAULT

def query_statement(flag=None) -> str:
     """QA for query artist statements"""
     if flag == 'QA':
          return SELECT_QUERY_ARTIST
     else: 
          return DEFAULT

