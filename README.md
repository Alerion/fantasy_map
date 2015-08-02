Map generator based on this [algo](http://www-cs-students.stanford.edu/~amitp/game-programming/polygon-map-generation/)

Run tiles erver:

    $ gunicorn "TileStache:WSGITileServer('tilestache.json')"

    or

    $ tilestache-server.py -c tilestache.json

Run web server:

    $ ./manage.py runserver 127.0.0.1:8001

# Installation

Requires Python 2.7.

Create virtualenv with --system-site-packages, it is problem to install mapnik into virtualenv.

    $ virtualenv-2.7 --system-site-packages env

## Install mapnik

From here: https://github.com/mapnik/mapnik/wiki/UbuntuInstallation:

    sudo add-apt-repository ppa:mapnik/nightly-2.3
    sudo apt-get update
    sudo apt-get install libmapnik libmapnik-dev mapnik-utils python-mapnik
    # also install datasource plugins if you need them
    sudo apt-get install mapnik-input-plugin-gdal mapnik-input-plugin-ogr\
      mapnik-input-plugin-postgis \
      mapnik-input-plugin-sqlite \
      mapnik-input-plugin-osm

## Install PostgreSQL

    $ sudo apt-get install postgresql-9.4 postgresql-contrib-9.4 libpq-dev

If packages are not available follow [this instruction](<http://www.postgresql.org/download/linux/ubuntu/>)
how to add repository. (Check Ubuntu version ``lsb_release -a``)

## Install GeoDjango, PostGIS and other

https://docs.djangoproject.com/en/1.8/ref/contrib/gis/install/

## Install requirements

    $ pip install -r requirements.txt

## Create database

    $ sudo su - postgres
    $ createdb fantasy_map
    $ createuser -P fantasy_map

        Enter password for new role: fantasy_map
        Enter it again: fantasy_map

    $ psql

        postgres=# GRANT ALL PRIVILEGES ON DATABASE fantasy_map TO fantasy_map;

    $ ./manage.py migrate
    $ ./manage.py import_map

## Usage

Generate tiles:

    $ ./manage.py create_tiles
