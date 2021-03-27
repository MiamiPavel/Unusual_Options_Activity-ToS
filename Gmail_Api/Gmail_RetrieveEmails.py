# Got from this guy
# https://www.youtube.com/watch?v=vgk7Yio-GQw
import pickle
import os.path
from apiclient import errors
import email
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import base64

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

# Authentication with google part
def get_service():
    """
    Authenticate the google api client and return the service object
    to make further calls
    PARAMS
        None
    RETURNS
        service api object from gmail for making calls
    """
    creds = None

    # print(os.listdir())

    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('../token.pickle'):
        print('token.pickle exists')
        with open('../token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print('Credentials expired, refreshing token')
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open('../token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    return service

# search for messages that match criteria and give back list of ID's
def search_message(service, user_id, search_string):
    """
    Search the inbox for emails using standard gmail search parameters
    and return a list of email IDs for each result
    PARAMS:
        service: the google api service object already instantiated
        user_id: user id for google api service ('me' works here if
        already authenticated)
        search_string: search operators you can use with Gmail
        (see https://support.google.com/mail/answer/7190?hl=en for a list)
    RETURNS:
        List containing email IDs of search query
    """
    service = get_service()
    try:
        # initiate the list for returning
        list_ids = []

        # get the id of all messages that are in the search string
        search_ids = service.users().messages().list(userId=user_id, q=search_string).execute()

        # if there were no results, print warning and return empty string
        try:
            ids = search_ids['messages']

        except KeyError:
            print("WARNING: the search queried returned 0 results")
            print("returning an empty string")
            return ""

        if len(ids) > 1:
            print("Found emails:" + str(len(ids)))
            for msg_id in ids:
                list_ids.append(msg_id['id'])
            print (list_ids)
            return (list_ids)

        else:
            list_ids.append(ids['id'])
            return list_ids

    except (errors.HttpError, error):
        print("An error occured: %s") % error

# parse ID's to get email content

def get_message(service, user_id, msg_id):
    """
    Search the inbox for specific message by ID and return it back as a
    clean string. String may contain Python escape characters for newline
    and return line.

    PARAMS
        service: the google api service object already instantiated
        user_id: user id for google api service ('me' works here if
        already authenticated)
        msg_id: the unique id of the email you need
    RETURNS
        A string of encoded text containing the message body
    """

    try:
        # grab the message instance
        message = service.users().messages().get(userId=user_id, id=msg_id, format='raw').execute()

        # Email Subject
        msg_subject = message['snippet']

        # decode the raw message body string, ASCII works pretty well here
        msg_str = base64.urlsafe_b64decode(message['raw'].encode('ASCII'))

        # grab the string from the byte object
        mime_msg = email.message_from_bytes(msg_str)

        # check if the content is multipart (it usually is)
        content_type = mime_msg.get_content_maintype()
        if content_type == 'multipart':
            # there will usually be 2 parts the first will be the body in text
            # the second will be the text in html
            parts = mime_msg.get_payload()

            # return the encoded text
            final_content = parts[0].get_payload()
            print("Returning text below-Checkpoint1:")
            return final_content

        elif content_type == 'text':
            print("Returning text below-Checkpoint2:")
            return mime_msg.get_payload()

        else:
            return ""
            print("\nMessage is not text or multipart, returned an empty string")
    # unsure why the usual exception doesn't work in this case, but
    # having a standard Exception seems to do the trick
    except Exception:
        print("An error occured: %s") % error


# magic string that makes it work :)
search_results = search_message(get_service(), 'me', 'alerts@thinkorswim.com UnusualOptionsActivity-20210323')

# How to split text by finding two strings
# confusing, have to look at
# https://www.programiz.com/python-programming/methods/string/find

latest_email_id = search_results[0] # looks at only latest string
print("Latest Email:")
print(latest_email_id)
startOfStringText = 'UnusualOptionsActivity-20210323:'
endOfStringText = '.'
latest_email_body = get_message(get_service(), 'me', latest_email_id)

startOfStringCharacterNumber = latest_email_body.find(startOfStringText)
endOfStringCharacterNumber = latest_email_body.find(endOfStringText, startOfStringCharacterNumber)

tickers_text = latest_email_body[startOfStringCharacterNumber:endOfStringCharacterNumber]
tickers_text = tickers_text[len(startOfStringText):] #split out the search string
tickers_text = tickers_text.replace('=', '')
tickers_text = tickers_text.replace(' ', '')

# .rstrip function can't remove /r/n inside of body of text
# this way works
tickers_text = tickers_text.splitlines()
tickers_text = ''.join(tickers_text)

ticker_list = tickers_text.split(",")
print("Ticker List:")
print(ticker_list)



