# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#
# import models as models
from models import *
from utils import *
import json
# import dateutil.parser
# import babel
import datetime
from flask import Flask, render_template, request, flash, redirect, url_for, Response
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from flask_migrate import Migrate
from forms import *
from config import *
from flask_cors import CORS
# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = init_app(app)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.jinja_env.filters['datetime'] = format_datetime
CORS(app)

# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  areas = db.session.query(Venue.city, Venue.state).distinct()
  data = []
  for venue in areas:
    venue = dict(zip(('city', 'state'), venue))
    venue['venues'] = []
    for venue_data in Venue.query.filter_by(city=venue['city'],state=venue['state']).all():
      shows = Show.query.filter_by(venue_id=venue_data.id).all()
      venues_data = {
          'id': venue_data.id,
          'name': venue_data.name,
          'num_upcoming_shows': len(upcoming_shows(shows))
      }
      venue['venues'].append(venues_data)
    data.append(venue)
  return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  venues = db.session.query(Venue.name, Venue.id).all()
  data = []
  
  for venue in venues:
    name = venue[0]
    id = venue[1]
    if name.find(request.form.get('search_term', '')) != -1:
      shows = Show.query.filter_by(venue_id=id).all()
      venue = dict(zip(('name', 'id'), venue))
      venue['num_upcoming_shows'] = len(upcoming_shows(shows))
      data.append(venue) 

  response = {
    "data": data,
    "count": len(data),
  }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  venue = Venue.query.filter_by(id=venue_id).first()
  shows = Show.query.filter_by(venue_id=venue_id).all()
  data = {
    "id": venue.id,
    "name": venue.name,
    "genres": venue.genres,
    "address": venue.address,
    "city": venue.city,
    "state": venue.state,
    "phone": venue.phone,
    "website": venue.website,
    "facebook_link": venue.facebook_link,
    "seeking_talent": venue.seeking_talent,
    "seeking_description": venue.seeking_description,
    "image_link": venue.image_link,
    "past_shows": past_shows(shows),
    "upcoming_shows": upcoming_shows(shows),
    "past_shows_count": len(past_shows(shows)),
    "upcoming_shows_count": len(upcoming_shows(shows))
  }
  return render_template('pages/show_venue.html', venue=data)

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  
  try:
    form = VenueForm()
    venue = Venue(
      name=form.name.data,
      city=form.city.data,
      state=form.state.data,
      address=form.address.data,
      phone=form.phone.data,
      genres=form.genres.data,
      facebook_link=form.facebook_link.data,
      website=form.website.data,
      image_link=form.image_link.data,
      seeking_talent=form.seeking_talent.data,
      seeking_description=form.seeking_description.data,
    )
    db.session.add(venue)
    db.session.commit()

    flash('Venue ' + request.form['name'] + ' was successfully listed!')
    return render_template('pages/home.html')
  except Exception as e:
    flash('An error occurred. Venue could not be listed.')
    db.session.rollback()
    return render_template('pages/home.html')
  finally:
    db.session.close()
      
  return render_template('pages/home.html')

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  venue = Venue.query.filter_by(id=venue_id).first()
  form = VenueForm(obj=venue)
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  try:
    form = VenueForm()
    venue = Venue.query.get(venue_id)
    venue.name = form.name.data
    venue.city = form.city.data
    venue.state = form.state.data
    venue.address = form.address.data
    venue.phone = form.phone.data
    venue.genres = form.genres.data
    venue.facebook_link = form.facebook_link.data
    venue.website = form.website.data
    venue.image_link = form.image_link.data
    venue.seeking_talent = form.seeking_talent.data
    venue.seeking_description = form.seeking_description.data
    db.session.commit()
    return redirect(url_for('show_venue', venue_id=venue_id))
  except Exception as e:
    flash('Error to edit venue' + request.form['name'])
    db.session.rollback()
    return redirect(url_for('show_venue', venue_id=venue_id))
  finally:
    db.session.close()

@app.route('/venues/<venue_id>/delete', methods=['POST'])
def delete_venue(venue_id):
  try:
    venue = Venue.query.get(venue_id)
    db.session.delete(venue)
    db.session.commit()
    return render_template('pages/venues.html')
  except Exception as e:
    print(e)
    flash('Could not delete the venue')
    db.session.rollback()
    return render_template('pages/venues.html')
  finally:
      db.session.close()

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  data = []
  artists = db.session.query(Artist.id, Artist.name).all()
  for artist in artists:
    artist = dict(zip(('id', 'name'), artist))
    data.append(artist)
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  artists = db.session.query(Artist.name, Artist.id).all()
  data = []
  for artist in artists:
    name = artist[0]
    id = artist[1]
    if name.find(request.form.get('search_term', '')) != -1:
      shows = Show.query.filter_by(artist_id=id).all()
      artist = dict(zip(('name', 'id'), artist))
      artist['num_upcoming_shows'] = len(upcoming_shows(shows))
      data.append(artist)

  response = {
    "data": data,
    "count": len(data)
  }

  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  try:
    form = ArtistForm()
    artist = Artist(
      name=form.name.data,
      city=form.city.data,
      state=form.state.data,
      phone=form.phone.data,
      genres=form.genres.data,
      facebook_link=form.facebook_link.data,
      website=form.website.data,
      image_link=form.image_link.data,
      seeking_venue=form.seeking_venue.data,
      seeking_description=form.seeking_description.data,
    )
    db.session.add(artist)
    db.session.commit()
    flash('Artist Created ' + artist.name)
    return render_template('pages/home.html')
  except Exception as e:
    flash(f"Error to create artists {request.form['name']}. Error: {e}")
    db.session.rollback()
    return render_template('pages/home.html')
  finally:
    db.session.close()

@app.route('/artists/<int:artist_id>', methods=['GET'])
def show_artist(artist_id):
  print("------------ddddddddddddddddd------")
  artist = Artist.query.filter_by(id=artist_id).first()
  shows = Show.query.filter_by(artist_id=artist_id).all()

  data = {
    "id": artist.id,
    "name": artist.name,
    # "genres": artist.genres.strip("{").strip("}").split(","),
    "genres": to_list(artist.genres),
    "city": artist.city,
    "state": artist.state,
    "phone": artist.phone,
    "website": artist.website,
    "facebook_link": artist.facebook_link,
    "seeking_venue": artist.seeking_venue,
    "seeking_description": artist.seeking_description,
    "image_link": artist.image_link,
    "past_shows": past_shows(shows),
    "upcoming_shows": upcoming_shows(shows),
    "past_shows_count": len(past_shows(shows)),
    "upcoming_shows_count": len(upcoming_shows(shows))
  }

  return render_template('pages/show_artist.html', artist=data)
  
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  artist = Artist.query.get(artist_id)
  form = ArtistForm(obj=artist)
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  try:
    form = ArtistForm()
    artist = Artist.query.get(artist_id)
    artist.name = form.name.data
    artist.city = form.city.data
    artist.state = form.state.data
    artist.phone = form.phone.data
    artist.genres = form.genres.data
    artist.facebook_link = form.facebook_link.data
    artist.website = form.website.data
    artist.image_link = form.image_link.data
    artist.seeking_venue = form.seeking_venue.data
    artist.seeking_description = form.seeking_description.data
    db.session.commit()
    return redirect(url_for('show_artist', artist_id=artist_id))
  except Exception as e:
    flash('Error to edit artist ' + request.form['name'])
    db.session.rollback()
    return redirect(url_for('show_artist', artist_id=artist_id))
  finally:
    db.session.close()

@app.route('/artists/<artist_id>/delete', methods=['POST'])
def delete_artist(artist_id):
  try:
    artist = Artist.query.get(artist_id)
    db.session.delete(artist)
    db.session.commit()
    return render_template('pages/artists.html')
  except Exception as e:
    print(e)
    flash(error_delete +' artist')
    db.session.rollback()
    return render_template('pages/artists.html')
  finally:
      db.session.close()

#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  shows = Show.query.all()
  data = []
  for show in shows:
    show = {
      "venue_id": show.venue_id,
      "venue_name": db.session.query(Venue.name).filter_by(id=show.venue_id).first()[0],
      "artist_id": show.artist_id,
      "artist_image_link": db.session.query(Artist.image_link).filter_by(id=show.artist_id).first()[0],
      "start_time": str(show.start_time)
    }
    data.append(show)
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  form = ShowForm()
  try:
    show = Show(
      venue_id=form.venue_id.data,
      artist_id=form.artist_id.data,
      start_time=form.start_time.data,
    )
    db.session.add(show)
    db.session.commit()
    flash('Show was successfully listed!')
    return render_template('pages/home.html')
  except Exception as e:
    flash(f'An error occurred. Show could not be listed. Error: {e}')
    db.session.rollback()
    return render_template('forms/new_show.html', form=form)
  finally:
    db.session.close()


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

# ----------------------------------------------------------------------------#
# Launch.
# ----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
