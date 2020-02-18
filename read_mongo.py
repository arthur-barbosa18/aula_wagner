from lxml import html
import requests
from pymongo import MongoClient
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


def read_mongo():
    client = MongoClient("localhost", 27017)
    dict_chinese = client.dictionary_chinese.dict_chi
    list_dict = []
    for i in dict_chinese.find({}):
        i["word"] = i["word"].decode("gb2312")
        del i["_id"]
        list_dict.append(i)

    return list_dict


for i in read_mongo():
    print(i)


def parse_res_mongo(list_dict):
    values = []
    for index_dict_values in range(0, len(list_dict)):
        if index_dict_values == 0:
            values.append([i for i in list_dict[index_dict_values].keys()])
            continue
        elif index_dict_values != (len(list_dict) - 1):
            values.append([i for i in list_dict[index_dict_values].values()])
            continue
        return values


bla = parse_res_mongo(read_mongo())


def write_google_sheet():
    spreadsheet_id = "1lgI9_8jKYFJcWaDkJ8kY12bdz5m5F7q6e72tuyXR_Cc"
    range_name = "La"
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    service = build("sheets", "v4", credentials=creds)

    # values = # deve ter a estrutura == [ [], [], [] ]
    values = parse_res_mongo(read_mongo())
    matrix_correct = []
    for i in values:
        values_correct = []
        for j in i:
            if type(j) is list:
                values_correct.append(", ".join(j))
                matrix_correct.append(values_correct)
                continue
            values_correct.append(j)
        matrix_correct.append(values_correct)

    body = {"values": matrix_correct}
    import ipdb

    ipdb.set_trace()  # breakpoint 12050c6e //

    result = (
        service.spreadsheets()
        .values()
        .update(valueInputOption="USER_ENTERED", spreadsheetId=spreadsheet_id, range=range_name, body=body)
        .execute()
    )
    print("{0} cells updated.".format(result.get("updatedCells")))


write_google_sheet()
