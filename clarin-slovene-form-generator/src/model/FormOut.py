from typing import List
from pydantic import BaseModel
from model.OrthographyOut import OrthographyOut


class FormOut(BaseModel):
    orthographies: List[OrthographyOut]
