import psycopg2
import config

DATABASE_NAME = config.DATABASE_NAME
POSTGRESQL_USER = config.POSTGRESQL_USER

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
