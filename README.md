## Running Epimobile using Docker 

After you've installed docker, run:

1. `docker build -t epimobile:latest .`

2. `docker run -p 5000:5000 epimobile`

If you want to run /bin/bash *inside* the container:

`docker run -i -t --rm epimobile /bin/bash`
