from typing import List
from pydantic import BaseModel

from model.AccentuationOut import AccentuationOut


class OrthographyOut(BaseModel):
    text: str
    morphologyPatterns: str
    accentuations: List[AccentuationOut]
