# WISHLIST use .dockerignore to generate excludes
build:
	tar --exclude='.*' --exclude='*.pyc' --exclude='examples' --dereference \
	  --to-stdout -cv * | docker build -t "texastribune/cloudviz" -


# The following only serve as examples/references for how you could use the image

run:
	docker run --name=cloudviz -p 5000:5000 --env-file=.env --detach texastribune/cloudviz

# Ctrl+p, Ctrl+q to detach
debug:
	docker attach cloudviz
