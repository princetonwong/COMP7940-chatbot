import logging
import psycopg2
from Utilities import parsePossibleListStringToListNew


class Database(object):
    def __init__(self):
        self.conn = psycopg2.connect(database="d8lo9ipulmq31b",
                                user='dlrggmpuyfznjv',
                                password='9e6cb5354edb6c3c6c6b4ecf0fa15b7b4c31397adc3f75f37d8417fa74cac98e',
                                host='ec2-52-205-45-222.compute-1.amazonaws.com',
                                port='5432'
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
        # keywords = parsePossibleListStringToListNew(searchString)

        sql = f"""SELECT code, englishname, chinesename
        FROM school
        WHERE CONCAT_WS(' - ', code, englishname, chinesename) LIKE '%{searchString}%'
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
        #     # from pydrive2.auth import GoogleAuth
        #     # from pydrive2.drive import GoogleDrive
        #     # from googleapiclient.discovery import build
        #     #
        #     # def connect_google_drive_api():
        #     #     gauth = GoogleAuth()
        #     #     gauth.LoadCredentialsFile("credentials.json")
        #     #     if gauth.credentials is None:
        #     #         # Authenticate if they're not there
        #     #         # This is what solved the issues:
        #     #         gauth.GetFlow()
        #     #         gauth.flow.params.update({'access_type': 'offline'})
        #     #         gauth.flow.params.update({'approval_prompt': 'force'})
        #     #         gauth.LocalWebserverAuth()
        #     #     elif gauth.access_token_expired:
        #     #         # Refresh them if expired
        #     #         gauth.Refresh()
        #     #     else:
        #     #         # Initialize the saved creds
        #     #         gauth.Authorize()
        #     #     gauth.SaveCredentialsFile("credentials.json")
        #     #     drive = GoogleDrive(gauth)
        #     #     creds = gauth.credentials
        #     #
        #     #     return drive, creds
        #     #
        #     # creds = None
        #     # drive, creds = connect_google_drive_api()
        #     # service = build('drive', 'v3', credentials=creds)
        #
        #     # Generate a download link for the file
        #     # file_link = service.files().get(fileId=partialFileID, fields='webContentLink').execute()['webContentLink'].replace('open', 'uc')
        #     # print(f"File name: {file_metadata['name']}")
        #     logging.info(f"Download link: {paper.gdrivelink}")
        #     return paper.gdrivelink
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

    record = db.getFileID("1gEae3G9s_ZAOKYHU4CN51I5yS9MN3OMx")
