#!/usr/bin/python
import MySQLdb
import sys

#A little class to help with any our mysql needs.  Right now it is a LITTLE redundant
class MySQLTools:
  def __init__(self,host,user,passwd,db):
	try:
  	  self.db = MySQLdb.connect(host,user,passwd,db)
	except Exception, e:
  	  print repr(e)
  	  sys.exit()
  def do_query(self,query):
	try:
  	  cur = self.db.cursor()
  	  cur.execute(query)
   	  return cur.fetchall()
	except Exception, e:
  	  print repr(e)
  	  sys.exit()

def main():
	print "main"


if __name__ == "__main__":
  main()
