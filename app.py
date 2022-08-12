

from email.contentmanager import ContentManager
import json
import dateutil.parser
import babel
from flask.wrappers import Response
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
from src.utils import process_dict,insert_into_db,genre_submission,get_id,v_genre_submission
from src.connect import data_conn
from src.handlerclass import ShowHandler
from src.fetch import get_list,get_venue_detail
from src.artist_fetch import get_artist_list,get_artist_detail
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#
#  TODO: implement genre addition
app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app,db)
# TODO: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(256))

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(256))

    # TODO: implement any missing fields, as a database migration using Flask-Migrate
class Show(db.Model):
    __tablename__ = 'show'

    id = db.Column(db.Integer,primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'))
    venue_id = db.Column(db.Integer,db.ForeignKey('venue.id'))
    start_time = db.Column(db.DateTime)

class Genre(db.Model):
    __tablename__ = 'genre'

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(120))

class ArtisteGenre(db.Model):
    __tablename__ = 'artiste_genre'

    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'),primary_key=True)
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.id'),primary_key=True)

class VenueGenre(db.Model):
    __tablename__ = 'venue_genre'

    genre_id = db.Column(db.Integer, db.ForeignKey('genre.id'),primary_key=True)
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'),primary_key=True)

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  data = get_list()
  # replaced by real venue data from database.
  return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on venues with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  search = request.form.get('search_term')
  query = """select venue.id,name,count(show.*) from venue left join show on venue.id = show.venue_id
              and name = %s"""
  con = data_conn()
  # data_conn util function from the connect module in the src folder
  cx = con.cursor()
  cx.execute(query,(search,))
  search_result = cx.fetchone()
  con.close()
  response={
    "count": 1,
    "data": search_result
  }

  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  data = get_venue_detail(venue_id)
  # NOTE: replaced with real data
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: modify data to be the data object returned from db insertion
  data,genres = process_dict(request.form)
  conn = data_conn()
  insert = insert_into_db(conn,data,'V')
  id = get_id(data)
  genre_added  = v_genre_submission(genres,id,conn,)
  if insert and genre_added:
    # on successful db insert, flash success
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
  else: 
    flash('Venue ' + request.form['name'] + ' could not be listed, and error occurred')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):

  query = """delete from venue where id = %s"""
  try:
    con = data_conn()
    cx = con.cursor()
    cx.execute(query,(venue_id,))
    con.commit()
    con.close()
  except Exception as err:
    print(err)
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  data = get_artist_list()
  # NOTE: replaced with real data.
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # search for "band" should return "The Wild Sax Band".
  search = request.form.get('search_term')
  con = data_conn()
  cx = con.cursor()
  cx.execute("""select artist.id,name,count(show.*) from artist left join show on artist.name like %s
  group by artist.id""",(search,))
  data = cx.fetchone()
  con.close()
  response={
    "count": 1,
    "term": '',
  }
  response.setdefault('data',[data])
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # NOTE: implemented real data from database.
  
  data = get_artist_detail(artist_id)
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  data = get_artist_detail(artist_id)
  return render_template('forms/edit_artist.html', form=form, artist=data)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  con = data_conn()
  cx = con.cursor()
  data = request.form
  proc,genres = process_dict(data)
  val = []
  for k,v in proc.items():
    val.append(v)
  vals = proc.values()
  query = """update artist set name = %s, city = %s, state = %s, image_link = %s, facebook_link = %s,
              website_link = %s, seeking_venue = %s, seeking_description = %s"""
  cx.execute(query,val)
  con.commit()
  con.close()
  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  con = data_conn()
  cx = con.cursor()
  query = """select * from venue where id = %s"""
  cx.execute(query,(venue_id,))
  venue = cx.fetchone()
  con.close()
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  con = data_conn()
  cx = con.cursor()
  data = request.form
  proc,genres = process_dict(data)
  val = []
  for k,v in proc.items():
    val.append(v)
  vals = proc.values()
  query = """update venue set name = %s, city = %s, state = %s, image_link = %s, facebook_link = %s,
              website_link = %s, seeking_talent = %s, seeking_description = %s"""
  cx.execute(query,val)
  con.commit()
  con.close()
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  # on successful db insert, flash success
  data = request.form
  conn = data_conn()
  proc_dict,genres = process_dict(data)
  # process the form data to primitive python dictionary
  # pass the connection object and the the processed dictionary to the insert db function...
  inserted = insert_into_db(conn,proc_dict)
  id = get_id(proc_dict)

  genre_added = genre_submission(genres,id,conn)
  
  if inserted and genre_added:
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
  else:
    flash('Artist could not be added due to an error')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  shows = ShowHandler.build_list()
  if shows:
    d = shows.get_convert_data()
  data = d
  
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  # on successful db insert, flash success
  conn = data_conn()
  # get the connection object
  data,ofl = process_dict(request.form)
  # process data to prim dict
  insert = insert_into_db(conn,data,flag='SH')
  
  if insert:
    flash('Show was successfully listed!')
  else: 
    flash('Show could not be listed, an error occurred')
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
