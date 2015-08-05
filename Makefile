clean:
	find . -name "*.pyc" -exec rm -rf {} \;

runserver:
	./manage.py runserver

runtileserver:
	tilestache-server.py -c tilestache.json

generate_map:
	./manage.py generate_map

import_import_countries:
	./manage.py import_countries

create_map_image:
	./manage.py create_map_image
