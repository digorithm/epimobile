import psycopg2

# TODO: extract this to a config file
# TODO: this is extremely coupled with the postgresql, make it loosely coupled in the future

DATABASE_NAME = "epimobile"
POSTGRESQL_USER = "rodrigo"

class BaseDB(object):

  def __init__(self, db_name=DATABASE_NAME, username=POSTGRESQL_USER):
    self.conn = psycopg2.connect("dbname={} user={}".format(db_name, username))
    self.cur = self.conn.cursor()

  def __del__(self):
    self.cur.close()
    self.conn.close()

  def insert(self, query, values):
    self.cur.execute(query, values)
    self.conn.commit()
    return self.cur.fetchone()[0]
  
  def update(self, query, values):
    self.cur.execute(query, values)
    self.conn.commit()

  def get(self, query, values):
    self.cur.execute(query, values)
    return self.cur.fetchall()
