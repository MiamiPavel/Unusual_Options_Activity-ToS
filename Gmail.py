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
            for msg_id in ids:
                list_ids.append(msg_id['id'])
            return (list_ids)

        else:
            list_ids.append(ids['id'])
            return list_ids

    except (errors.HttpError, error):
        print("An error occured: %s") % error


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
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    return service

search_results = search_message(get_service(), 'me', 'alerts@thinkorswim.com UnusualOptionsActivity-20210323')


# def my_string():
#     # text at start of target string of tickers
#     startOfStringText = 'UnusualOptionsActivity-20210323:'
#     # text at end of target string of tickers
#     endOfStringText = '.'
#     return print(str.find(latest_email,startOfStringText,endOfStringText))

###################
# Example 2: find() With start and end Arguments
# quote = 'Do small things with great love'
#
# # Substring is searched in 'hings with great love'
# print(quote.find('small things', 10))
#
# # Substring is searched in ' small things with great love'
# print(quote.find('small things', 2))
#
# # Substring is searched in 'hings with great lov'
# print(quote.find('o small ', 10, -1))
#
# # Substring is searched in 'll things with'
# print(quote.find('things ', 6, 20))
################

# How to split text by finding two strings
# confusing, have to look at
# https://www.programiz.com/python-programming/methods/string/find

latest_email_id = search_results[0]
startOfStringText = 'UnusualOptionsActivity-20210323:'
endOfStringText = '.'
latest_email_body = get_message(get_service(), 'me', latest_email_id)
#print(str.find(latest_email,startOfStringText,endOfStringText))

startOfStringCharacterNumber = latest_email_body.find(startOfStringText)
endOfStringCharacterNumber = latest_email_body.find(endOfStringText, startOfStringCharacterNumber)

latest_email_body.split(startOfStringCharacterNumber:endOfStringCharacterNumber)
print(latest_email_body)

#print(my_string)


