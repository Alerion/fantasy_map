Map generator based on this [article](http://www-cs-students.stanford.edu/~amitp/game-programming/polygon-map-generation/).

## Usage

See Makefile

It is is not necessary to install Mapnik, PostgreSQL and other staff to work with generator.
You can run `make generate_map` and see result in matplotlib chart.

# Installation

Requires Python 2.7.

Create virtualenv with --system-site-packages(it is problem to install mapnik into virtualenv).

    $ virtualenv-2.7 --system-site-packages env

## Install mapnik

Follow this https://github.com/mapnik/mapnik/wiki/UbuntuInstallation. Tested with mapnik 2.3

## Install PostgreSQL

    $ sudo apt-get install postgresql-9.4 postgresql-contrib-9.4 libpq-dev

If packages are not available follow [this instruction](<http://www.postgresql.org/download/linux/ubuntu/>)
how to add repository. (Check Ubuntu version ``lsb_release -a``)

## Install GeoDjango, PostGIS, GDAL and other

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
