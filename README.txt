FixCity aka BikeRaction aka BuildMeABikeRack
============================================

This is the code behind http://fixcity.org/ , a site that aims to help
get bike racks built in New York City, by allowing ordinary people to
combine efforts and get bulk orders submitted to the NYC Department of
Transportation.

It was built by OpenPlans, http://openplans.org.

The canonical source code is at http://github.com/openplans/fixcity

The project wiki is at https://projects.openplans.org/fixcity/wiki
and the bug tracker is at https://projects.openplans.org/fixcity/report

There is a #fixcity IRC channel on irc.freenode.net, although it's
not very active (as of December 2010).

What's In a Name?
-----------------

This project has been through several names already. Sorry :)

If you see "bmabr" in code, it's just an acronym for "Build Me A Bike
Rack", one of the older names. Don't worry about it...


License
=======


Released under the terms of the GNU Affero General Public License (GNU
AGPL). See COPYING.txt for details.


INSTALLATION
=============

Prerequisites
-------------

Things you will need.

On Ubuntu 9.04 - 9.10::

 sudo apt-get install \
  build-essential \
  libgeos-dev \
  libjpeg-dev \
  libpq-dev \
  libxml2-dev \
  libxslt1-dev \
  postgis \
  postgresql-8.3 \
  postgresql-server-dev-8.3 \
  proj \
  python \
  python-dev

postgresql-8.4 also should work.

I had some trouble on Ubuntu 9.10; I was able to proceed by installing
postgis from source according to the instructions here:
http://biodivertido.blogspot.com/2009/10/install-postgresql-84-and-postgis-140.html

Add info for other systems here...


Installation
------------

Given all the prerequisites above, just run ``python setup.py develop``,
preferably in a virtualenv to avoid installing stuff into your global
python site-packages.

(There is also a pip requirements file if you want to use pip to get a
known-working set of package versions.  Do ``pip install -r
pip-requirements.txt && python setup.py develop``)


Bootstrapping a Database
------------------------

This application requires a PostGIS database and some shape data. To
get started:

1) Copy the config.ini.in file to config.ini.  Edit database settings
   in config.ini as needed.  You MUST change the value of the
   'SECRET_KEY' setting.

2) Create your database::

    createdb -T template_postgis bmabr

   ... the last parameter should be the name of your database.  If you
   don't have a template_postgis database, Google will tell you how to
   create one ;)

3) Bootstrap the django models::

    cd fixcity
    ./manage.py syncdb
    ./manage.py migrate

4) (optional) Load the NYC data we use on fixcity.org. This can take a
   long time, several minutes at least::

   ./manage.py loaddata bmabr/fixtures/fixcity_org_nyc_data.json.gz
   ./manage.py loaddata bmabr/fixtures/fixcity_org_nyc_streets_data.json.gz

5) Visit the /admin/sites/site UI to change the domain name and
   display name of the website. These are used eg. in account
   confirmation email sent to users who register.


Testing
========

Just do::

  ./manage.py test bmabr

Exporting Bulk Orders
=====================

This feature is still in flux; as of 2010-12-15, there is a web UI
that isn't linked to from anywhere, and a command-line command you can
probably use more reliably/conveniently.  Just do ``manage.py
make_bulkorder <boroughname> <community board number>``.


Deployment
==========

If you want to deploy under mod_wsgi, there's an appropriate handler
script in fixcity/wsgi/.  Point your apache config at it, something
like this::


 <VirtualHost ...>
 ServerName ...
 
 <Directory /PATH/TO/fixcity/wsgi/>
    Order allow,deny
    Allow from all
 </Directory>
 
 WSGIScriptAlias / /PATH/TO/fixcity/wsgi/fixcity.wsgi
 
 </VirtualHost>


