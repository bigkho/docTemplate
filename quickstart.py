from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from datetime import datetime

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/documents',
'https://www.googleapis.com/auth/drive',
'https://www.googleapis.com/auth/drive.file']
# The ID of a sample document.


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
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('docs', 'v1', credentials=creds)
    drive_service = build('drive', 'v3', credentials=creds)

    #Retrieve the documents contents from the Docs service.
    copy_title = raw_input("Title of document: ")
    body = {
        'name': copy_title
    }
    drive_response = drive_service.files().copy(
    fileId='1WcsmyjZPrTm34DPMARhquJH1fgJ1m7blf_2b4aFtXLg', body=body).execute()
    document_copy_id = drive_response.get('id')
    print("...Created file...")

    TITLE = raw_input("title: ")
    AUTHOR = raw_input("author: ")
    PARAGRAPH = raw_input("paragraph: ")
    QUESTION = raw_input("question: ")

    #datetime.now().strftime("%m/%d/%Y")

    requests = [
         {
            'replaceAllText': {
                'containsText': {
                    'text': '{{TITLE}}',
                    'matchCase':  'true'
                },
                'replaceText': TITLE,
            }
        },
        {
           'replaceAllText': {
               'containsText': {
                   'text': '{{AUTHOR}}',
                   'matchCase':  'true'
               },
               'replaceText': AUTHOR,
           }
       },
       {
          'replaceAllText': {
              'containsText': {
                  'text': '{{PARAGRAPHS}}',
                  'matchCase':  'true'
              },
              'replaceText': PARAGRAPH,
          }
        },
        {
            'replaceAllText': {
                'containsText': {
                    'text': '{{QUESTION}}',
                    'matchCase':  'true'
                },
                'replaceText': QUESTION,
            }
        }
    ]
    result = service.documents().batchUpdate(documentId=document_copy_id, body={'requests': requests}).execute()
    print("Document finalized")

if __name__ == '__main__':
    main()
