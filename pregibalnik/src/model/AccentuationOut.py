from typing import List
from pydantic import BaseModel

from model.PronunciationOut import PronunciationOut


class AccentuationOut(BaseModel):
    text: str
    type: str
    pronunciations: List[PronunciationOut]
