from typing import Optional
from pydantic import BaseModel, constr


class AccentuatedFormIn(BaseModel):
    text: constr(min_length=1)
    msd: Optional[str] = ""
    morphologyPattern: Optional[str] = ""
