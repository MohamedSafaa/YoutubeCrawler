from __future__ import print_function
import mysql.connector
from mysql.connector import errorcode

class DBConnection:
	@staticmethod
	def get_active_connection():
		cnx = mysql.connector.connect(user='root', password='123456',
                              		      host='127.0.0.1')

		cursor = cnx.cursor()

		'''we check for the database if not exist we create new one then check for the table if not exist we creaet new one '''

		db_name = "youtube"
		try:
    			cnx.database = db_name
		except mysql.connector.Error as err:
    			if err.errno == errorcode.ER_BAD_DB_ERROR:
        			cursor.execute("CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(db_name))
        			cnx.database = db_name
    			else:
        			print(err)
        			exit(1)


		try:
    			cursor.execute("create table videos ("
    			"  `id` int NOT NULL AUTO_INCREMENT,"
			"  `video_id` varchar(20) NOT NULL,"
    			"  `views` int NOT NULL,"
    			"  `duration` varchar(20) NOT NULL,"
    			"  `title` varchar(50) NOT NULL,"
    			"  `video_url` varchar(100) NOT NULL,"
			"  `thumbnail_url` varchar(100) NOT NULL,"
			"  `original_image_url` varchar(100) NOT NULL,"
    			"  PRIMARY KEY (`id`)"
    			") ENGINE=InnoDB") # InnoDB for making commit

		except mysql.connector.Error as err:
    			if (err.errno != errorcode.ER_TABLE_EXISTS_ERROR):
        			print(err.msg)
		else:
    			print("the table is created successfully")
		return cnx , cursor

