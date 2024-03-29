# -*- coding: utf-8 -*-

from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import json

from time import sleep

import random


# If modifying these scopes, delete the file token.pickle.
#SCOPES = ['https://www.googleapis.com/auth/documents.readonly']
SCOPES = ['https://www.googleapis.com/auth/youtube.readonly']

# The ID of a sample document.
#DOCUMENT_ID = '195j9eDD3ccgjQRttHhJPymLJUCOUjs-jmwTrekvdjFE'

#DOCUMENT_ID = 'PL1eetAVZEtq-R6GdNJS8bomUS7063vzEq'

DOCUMENT_ID = 'PLbJEo9pUUei4RnMOsgZPZdANqQHWJzHu2'


URL='https://www.youtube.com/watch?v='


def main():
    """Shows basic usage of the Docs API.
    Prints the title of a sample document.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=9090)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('youtube', 'v3', credentials=creds)

    # Retrieve the documents contents from the Docs service.
    #document = service.documents().get(documentId=DOCUMENT_ID).execute()
    video_list = service.playlistItems()
    request = video_list.list(part="snippet", playlistId=DOCUMENT_ID, maxResults=10, fields='items/snippet(title, description, resourceId)')

    #print(json.dumps(document, indent=4))

    lista = []


    while request is not None:
        videos = request.execute()
        items = videos.get("items", [])
        request = video_list.list_next(request, videos)

        for item in items:
            #print( 'Video title: ', item["snippet"]["title"],  URL + str(item["snippet"]["resourceId"]["videoId"]) )
            video = {'title': item["snippet"]["title"], 'url': URL + str(item["snippet"]["resourceId"]["videoId"])}
            lista.append(video)

        sleep(2)

    dic = random.choice(lista)

    print(dic["title"], dic["url"])

if __name__ == '__main__':
    main()
