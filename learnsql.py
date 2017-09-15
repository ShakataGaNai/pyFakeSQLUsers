#!/usr/bin/python
# Make sure you install the pre-reqs:
# sudo apt-get install python-pip python-dev libmysqlclient-dev
# pip install MySQL-python requests

dbuser = 'learnsql'
dbpass = 'password'
db = 'learnsql'
numOfRecords = 500

from warnings import filterwarnings
import requests
import MySQLdb
conn = MySQLdb.connect(host="localhost",
                     user=dbuser,
                     passwd=dbpass,
                     db=db,
                     charset='utf8')

cur = conn.cursor()
filterwarnings('ignore', category = MySQLdb.Warning)

# ---------------------------

def createtbl(cur):
    try:
        cur.execute( """ 
CREATE TABLE IF NOT EXISTS `sampleusers` (
  `userid` int(11) NOT NULL AUTO_INCREMENT,
  `username` tinytext NOT NULL,
  `password` tinytext NOT NULL,
  `passsha256` tinytext NOT NULL,
  `firstname` tinytext NOT NULL,
  `lastname` tinytext NOT NULL,
  `email` tinytext NOT NULL,
  `gender` tinytext NOT NULL,
  `street` tinytext NOT NULL,
  `city` tinytext NOT NULL,
  `state` tinytext NOT NULL,
  `zip` tinytext NOT NULL,
  `lastupdate` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00' ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`userid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ; """ )
    except mysql.connector.Error as err:
        print("failed to create table: {}".format(err))
        exit(1)

def doFakeData(cur,url):
    r = requests.get(url)
    d = r.json()
    for l in d['results']:
        print("Inserting {} {}".format(l['name']['first'], l['name']['last']))
        personsql = ( """ INSERT INTO `learnsql`.`sampleusers` 
 (`userid`, `username`, `password`, `passsha256`, `firstname`, `lastname`,
 `email`, `gender`, `street`, `city`, `state`, `zip`, `lastupdate`) VALUES
 (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NULL); """ )
        persondata = (l['login']['username'], l['login']['password'], l['login']['sha256'],
                      l['name']['first'], l['name']['last'], l['email'], l['gender'],
                      l['location']['street'], l['location']['city'], l['location']['state'], l['location']['postcode'])
        cur.execute(personsql, persondata)
 

def main(conn,cur,qty):
    print("Getting started creating table")
    createtbl(cur)
    print("Getting & Saving {} records".format(qty))
    doFakeData(cur, 'https://randomuser.me/api?results={}&nat=us'.format(qty))
    print("All done! So long and thanks for all the fish.")
    conn.commit()
    cur.close()
    conn.close()

# -------------------
main(conn, cur, numOfRecords)
