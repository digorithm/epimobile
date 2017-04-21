/usr/lib/postgresql/9.3/bin/postgres -D /var/lib/postgresql/9.3/main -c config_file=/etc/postgresql/9.3/main/postgresql.conf &
sleep 5 &&
python src/scripts/init_database.py &&
python src/app.py