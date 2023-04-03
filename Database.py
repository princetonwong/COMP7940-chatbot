import logging
import os

import psycopg2
from Utilities import parsePossibleListStringToListNew


class Database(object):
    def __init__(self):
        self.conn = psycopg2.connect(database=os.environ["POSTGRES_DATABSE"], #"d8lo9ipulmq31b",
                                user=os.environ["POSTGRES_USER"], #'dlrggmpuyfznjv',
                                password=os.environ["POSTGRES_PASSWORD"], #'9e6cb5354edb6c3c6c6b4ecf0fa15b7b4c31397adc3f75f37d8417fa74cac98e',
                                host=os.environ["POSTGRES_HOST"], #'ec2-52-205-45-222.compute-1.amazonaws.com',
                                port= os.environ["POSTGRES_PORT"], #'5432'
                                )

        self.conn.autocommit = True
        self.cursor = self.conn.cursor()

    def importPaperCSV(self):
        sql = '''CREATE TABLE Paper(name varchar(80) NOT NULL,\
        fileType varchar(4),\
        fileSize integer,\
        fileID varchar(50))'''

        self.cursor.execute(sql)

        # psql -h "ec2-52-205-45-222.compute-1.amazonaws.com" -U "dlrggmpuyfznjv" -d "d8lo9ipulmq31b" -c "\copy Paper FROM '/Users/princetonwong/PycharmProjects/chatbot/SchoolPaper.csv' with (format csv,header true, delimiter ',');"

    def importSchoolCSV(self):
        sql = '''CREATE TABLE School(code varchar(80) NOT NULL,\
        englishName text,\
        chineseName text)'''

        self.cursor.execute(sql)

        # psql -h "ec2-52-205-45-222.compute-1.amazonaws.com" -U "dlrggmpuyfznjv" -d "d8lo9ipulmq31b" -c "\copy school FROM '/Users/princetonwong/PycharmProjects/chatbot/Schools.csv' with (format csv,header true, delimiter ',');"

    def searchSchool(self, searchString):
        keywords = parsePossibleListStringToListNew(searchString)

        subquery = ""
        for index, kw in enumerate(keywords):
            subquery += f"CONCAT_WS(' - ', code, englishname, chinesename) like '%{kw}%'"
            if index != len(keywords) - 1:
                subquery += " and "

        sql = f"""SELECT code, englishname, chinesename
        FROM school
        WHERE ({subquery})
        ORDER BY code;"""

        self.cursor.execute(sql)
        records = self.cursor.fetchall()

        return records

    def searchPaper(self, searchString):
        keywords = parsePossibleListStringToListNew(searchString)

        # sql = f"""SELECT *
        # FROM paper
        # WHERE CONCAT_WS(' - ', code, englishname, chinesename) LIKE '%{searchString}%'
        # ORDER BY code;"""

        # placeholders = ','.join(['%s'] * len(keywords))

        subquery = ""
        for index, kw in enumerate(keywords):
            subquery += f"name like '%{kw}%'"
            if index != len(keywords) - 1:
                subquery += " and "

        query_string = f"""
        SELECT *
        FROM paper
        WHERE ({subquery})
        """

        self.cursor.execute(query_string)
        records = self.cursor.fetchall()
        self.cursor.close()

        return records

    def getFileID(self, partialFileID):
        query_string = f"""
        SELECT *
        FROM paper
        WHERE fileid LIKE '%{partialFileID}%'
        """

        self.cursor.execute(query_string)
        args = self.cursor.fetchone()
        self.cursor.close()

        return args

        # if args:
        #     from googleapiclient.discovery import build
        #     import os
        #     import google.auth
        #     from google.auth.transport.requests import Request
        #     from google.oauth2.credentials import Credentials
        #     from google_auth_oauthlib.flow import InstalledAppFlow
        #     from googleapiclient.discovery import build
        #     from googleapiclient.errors import HttpError
        #     import io
        #     from googleapiclient.http import MediaIoBaseDownload
        #
        #     creds, _ = google.auth.default()
        #     service = build('drive', 'v3', credentials=creds)
        #
        #     def connect_google_drive_api():
        #         creds = None
        #         SCOPES = ['https://www.googleapis.com/auth/drive.file']
        #         # The file token.json stores the user's access and refresh tokens, and is
        #         # created automatically when the authorization flow completes for the first
        #         # time.
        #         if os.path.exists('token.json'):
        #             creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        #         # If there are no (valid) credentials available, let the user log in.
        #         if not creds or not creds.valid:
        #             if creds and creds.expired and creds.refresh_token:
        #                 creds.refresh(Request())
        #             else:
        #                 flow = InstalledAppFlow.from_client_secrets_file(
        #                     'credentials-desktop.json', SCOPES)
        #                 creds = flow.run_local_server(port=0)
        #             # Save the credentials for the next run
        #             with open('token.json', 'w') as token:
        #                 token.write(creds.to_json())
        #
        #         try:
        #             service = build('drive', 'v3', credentials=creds)
        #             return service, creds
        #
        #         except HttpError as error:
        #             # TODO(developer) - Handle errors from drive API.
        #             print(f'An error occurred: {error}')
        #
        #     # service, creds = connect_google_drive_api()
        #     file_id = args[-1]
        #     local_path = f'./{file_id}.pdf'
        #
        #     try:
        #         request = service.files().get_media(fileId=file_id)
        #         file = io.BytesIO()
        #         downloader = MediaIoBaseDownload(file, request)
        #         done = False
        #         while done is False:
        #             status, done = downloader.next_chunk()
        #             print(F'Download {int(status.progress() * 100)}.')
        #
        #
        #     except HttpError as error:
        #         print(F'An error occurred: {error}')
        #         file = None
        #
        #     # Write the file data to a local file
        #     with open(local_path, 'wb') as f:
        #         f.write(file.getbuffer())
        #
        #     return args, file.getvalue()
        #
        #     # # Generate a download link for the file
        #     # print(args)
        #     # file = service.files().get(fileId=args[-1], fields='webContentLink').execute()
        #     # print(file)
        #     # file_link = file['webContentLink'].replace('open', 'uc')
        #     # print(file_link)
        #     # logging.info(f"Download link: {file_link}")
        #     # return file_link
        # else:
        #     return None

if __name__ == "__main__":
    from School import School
    from Paper import Paper
    db = Database()
    # records = db.searchSchool("SCC")
    # count = len(records)
    # schools = [School(*kwargs) for kwargs in records]
    # print(schools)

    # records = db.searchPaper("SingYin,F1")
    # papers = [Paper(*args) for args in records]
    # print(papers[0].human_readable_size)

    record = db.getFileID("1WXJGXVOxFeJdstBjuIVe")
