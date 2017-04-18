import os

DATABASE_NAME = os.getenv("DATABASE_NAME", "epimobile")

# rodrigo is the default username in my machine. If you're running with Docker, then Dockerfile will be setting env var properly
POSTGRESQL_USER = os.getenv("POSTGRESQL_USER", "rodrigo")