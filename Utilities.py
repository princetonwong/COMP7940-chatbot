import csv

def parsePossibleListStringToListNew(txt: str) -> list:
    try:
        txt = [l for l in csv.reader(txt.splitlines(), quotechar='"', delimiter=',', quoting=csv.QUOTE_ALL,
                                     skipinitialspace=True)][0]
    except:
        txt = list()
    return txt