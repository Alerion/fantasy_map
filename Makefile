clean:
	find . -name "*.pyc" -exec rm -rf {} \;

runserver:
	./manage.py runserver

# Run with Python 2.7
runtileserver:
	tilestache-server.py -c tilestache.json

generate_map:
	./manage.py generate_map

generate_large_map:
	./manage.py generate_map --points=4000 --heights_map_width=3000 --hill_noise=true

create_map_image:
	python2.7 create_map_image.py
