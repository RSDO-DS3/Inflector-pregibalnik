from typing import List
from pydantic import BaseModel
from model.FormOut import FormOut


class MsdEntryOut(BaseModel):
    msd: str
    forms: List[FormOut]
