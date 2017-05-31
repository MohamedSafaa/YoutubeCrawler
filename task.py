import httplib2
import os
import sys
import time
import re

from apiclient.discovery import build
from Video import Video
from apiclient.errors import HttpError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow

CLIENT_SECRETS_FILE = "client_secret.json"

YOUTUBE_READONLY_SCOPE = "https://www.googleapis.com/auth/youtube.readonly"

#YOUTUBE_READ_WRITE_SCOPE = "https://www.googleapis.com/auth/youtube"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please configure OAuth 2.0

To make this sample run you will need to populate the client_secrets.json file
found at:
   %s
with information from the APIs Console
https://console.developers.google.com

For more information about the client_secrets.json file format, please visit:
https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
""" % os.path.abspath(os.path.join(os.path.dirname(__file__),
                                   CLIENT_SECRETS_FILE))
updates_list=[]


def get_authenticated_service():
  flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE, scope=YOUTUBE_READONLY_SCOPE,
    message=MISSING_CLIENT_SECRETS_MESSAGE)
  storage = Storage("%s-oauth2.json" % sys.argv[0])
  credentials = storage.get()

  if credentials is None or credentials.invalid:
    flags = argparser.parse_args()
    credentials = run_flow(flow, storage, flags)

  return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    http=credentials.authorize(httplib2.Http()))





# here we get the video details using the video id
def get_videos_details(youtube, video_id):
  results = youtube.videos().list(
    part="snippet,contentDetails,statistics",
    id=video_id,
  ).execute()
  video_url = "https://www.youtube.com/watch?v="+video_id
  title = results["items"][0]["snippet"]["title"]
  thumbnail_url = results["items"][0]["snippet"]["thumbnails"]["default"]["url"] 
  original_image_url = results["items"][0]["snippet"]["thumbnails"]["high"]["url"]
  duration = results["items"][0]["contentDetails"]["duration"]
  views = results["items"][0]["statistics"]["viewCount"]

  video = Video(video_id,views,duration,title,video_url,thumbnail_url,original_image_url)
  updates_list.append(video.add_video())



# here we get the playlist id using the channel name
def get_videos(youtube,channel_name):
  results = youtube.channels().list(
    part="snippet,contentDetails",
    forUsername=channel_name,
  ).execute()
  playlist_id = results["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
  get_playlist_videos(youtube,playlist_id)
  



# here we get the videos ids using the playlist id
def get_playlist_videos(youtube,playlist_id):
  playlistitems_list_request = youtube.playlistItems().list(
    playlistId=playlist_id,
    part="snippet",
    maxResults=50
  )


# while loop and using list_next() method because the max result can not be greater than 50
  while playlistitems_list_request:
     playlistitems_list_response = playlistitems_list_request.execute()

     for playlist_item in playlistitems_list_response["items"]:
       title = playlist_item["snippet"]["title"]
       video_id = playlist_item["snippet"]["resourceId"]["videoId"]
       get_videos_details(youtube,video_id)
     playlistitems_list_request = youtube.playlistItems().list_next(
       playlistitems_list_request, playlistitems_list_response)



def perform_program(youtube , param , target_function):
	global updates_list
	while(True):
  			try:
    	   			target_function(youtube, param)
  			except HttpError, e:
           			exit("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
			if(True in updates_list):
				print("There is new updates ...")
			else :
				print("No updates available ...")
			updates_list=[]
			time.sleep(10)


if __name__ == "__main__":
  print("choose what do you want to enter : ")
  print("1- channel url")
  print("2- playlist url")
  num=int(input("Enter the number:"))
  url=raw_input("Enter the url : ")
  youtube = get_authenticated_service()
  if(num == 1):
	com = re.search('[/]user[/](\w+)[/]?', url)
	if com :
		channel_name = com.group(1)
		perform_program(youtube,channel_name,get_videos)
	else :
		print("you entered a not valid url format, the format must be as the challange pdf illustrates.")
  elif(num==2):
	com = re.search('list[=](.+)', url)
	if com :
		playlist_id = com.group(1)
		perform_program(youtube,playlist_id,get_playlist_videos)

	else :
		print("you entered a not valid url format, the format must be as the challange pdf illustrates.")

  else :
	print("sorry you entered invalid number, please try again.")
