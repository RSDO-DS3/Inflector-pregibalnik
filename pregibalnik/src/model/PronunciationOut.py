from typing import List
from pydantic import BaseModel

from model.PronunciationFormOut import PronunciationFormOut


class PronunciationOut(BaseModel):
    forms: List[PronunciationFormOut]
