# pip install –upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os.path
import base64
import email
from bs4 import BeautifulSoup



