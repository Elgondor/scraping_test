from dataclasses import dataclass

@dataclass
class ScrapedData:
    registrant: str
    status: str
    class_type: str
    practice_location: str

    def to_dict(self):
        return {
            'registrant': self.registrant,
            'status': self.status,
            'class_type': self.class_type,
            'practice_location': self.practice_location,
        }
