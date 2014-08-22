# WISHLIST use .dockerignore to generate excludes
build:
	tar --exclude='.*' --exclude='*.pyc' --exclude='examples' --dereference \
	  --to-stdout -cv * | docker build -t "texastribune/cloudviz" -

run:
	docker run --name=cloudviz -p 5000:5000 --env-file=.env texastribune/cloudviz
