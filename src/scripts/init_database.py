import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import sys

DATABASE_NAME = "epimobile"
POSTGRESQL_USER = "rodrigo"

try:
  # Check if database already exists

  conn = psycopg2.connect("dbname=postgres user={}".format(POSTGRESQL_USER))

  cur = conn.cursor()
  cur.execute("SELECT exists(SELECT 1 from pg_catalog.pg_database where datname = %s)", (DATABASE_NAME,))
  
  db_exists = cur.fetchone()[0]

except psycopg2.DatabaseError, e:
  print "Error %s" %e
  sys.exit(1)

if db_exists:
  print "Epimobile DB already exists"
  sys.exit(1)
else:
  db = ("CREATE DATABASE {} "
        "WITH OWNER = {} "
        "ENCODING = 'UTF8' "
        "TABLESPACE = pg_default "
        "LC_COLLATE = 'en_US.UTF-8' "
        "LC_CTYPE = 'en_US.UTF-8' "
        "CONNECTION LIMIT = -1;".format(DATABASE_NAME, POSTGRESQL_USER))
  
  conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

  # Create epimobile database
  cur.execute(db)

  conn.commit()

  cur.close()
  conn.close()

  # Connect to new database 
  conn = psycopg2.connect("dbname={} user={}".format(DATABASE_NAME, POSTGRESQL_USER))

  cur = conn.cursor()

  sample_result_table = ("CREATE TABLE sample_result ("
                         "id serial NOT NULL,"
                         "sample_id varchar(45) NOT NULL,"
                         "highest_match text);")

  mash_output_table   = ("CREATE TABLE mash_output ("
                         "sample_result_id integer,"
                         "reference_id varchar(255) NOT NULL,"
                         "query_id varchar(255) NOT NULL,"
                         "mash_distance real NOT NULL,"
                         "p_value numeric(32, 30) NOT NULL,"
                         "matching_hashes varchar(10) NOT NULL);")
  
  
  cur.execute(sample_result_table)
  cur.execute(mash_output_table)

  conn.commit()
                        
  cur.close()
  conn.close()


