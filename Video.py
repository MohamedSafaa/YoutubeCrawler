from DBConnection import DBConnection
class Video:
      def __init__(self,video_id, views, duration , title , video_url,thumbnail_url,original_image_url):
	  self.video_id = video_id
      	  self.views = views
          self.duration = duration
          self.title = title
	  self.video_url = video_url
	  self.thumbnail_url=thumbnail_url
	  self.original_image_url=original_image_url

      
	
      def add_video(self):
	  cnx , cursor = DBConnection.get_active_connection()
	  if(not self.search_video()):
		add_video = ("INSERT INTO videos "
               "(video_id,views, duration, title, video_url,thumbnail_url,original_image_url) "
               "VALUES (%s, %s, %s , %s , %s, %s , %s)")
		video_data = (self.video_id, self.views, self.duration, self.title,self.video_url,self.thumbnail_url,self.original_image_url)
		cursor.execute(add_video,video_data)
		added_id = cursor.lastrowid
		cnx.commit()
		cursor.close()
          	cnx.close()
		return True
	  else:
		cursor.close()
          	cnx.close()
		return False

	  
      
      
      def search_video(self):
	  cnx , cursor = DBConnection.get_active_connection()
	  query = ("SELECT id FROM videos WHERE video_id ='"+self.video_id+"'")
	  cursor.execute(query)
          for id in cursor:
		cursor.close()
                cnx.close()
    	  	return True
	  cursor.close()
          cnx.close()
	  return False


