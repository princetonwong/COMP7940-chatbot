from dataclasses import dataclass

@dataclass
class School:
    code: str
    englishname: str
    chinesename: str

    @property
    def description(self):
        return