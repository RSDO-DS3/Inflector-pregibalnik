from typing import Optional

from pydantic import BaseModel


class WordIn(BaseModel):
    lema: str
    msd: str
    patternCode: Optional[str]
