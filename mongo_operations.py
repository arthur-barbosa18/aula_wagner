from pymongo import MongoClient

import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import numpy as np

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1q7Rh8_VqrLyjZAvPtnnb2sBaL1xdrkAk1hbs2QiCSro'
SAMPLE_RANGE_NAME = 'Jennifer!A2:E50'

def read_sheets():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
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

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])
    
    if not values:
        print('No data found.')
        return False
    return values


sheet = read_sheets()

dictionary_arr = []
dictionary = {}
for line in sheet:
    dictionary["English"] = line[0]
    dictionary["Pinyin"] = line[1]
    dictionary["Hanzi (S)"] = line[2]
    dictionary["Hanzi (T)"] = line[3]
    dictionary["Example"] = line[4]
    dictionary_arr.append(dictionary)

client = MongoClient("localhost", 27017)

database = client.dict_chinese

dict_chinese = database.xablau


la = dict_chinese.insert_many(dictionary_arr)