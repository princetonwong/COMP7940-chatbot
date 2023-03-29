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

if __name__ == "__main__":
    from School import School
    db = Database()
    records = db.searchSchool("SCC")
    count = len(records)
    schools = [School(*kwargs) for kwargs in records]
    print(schools)