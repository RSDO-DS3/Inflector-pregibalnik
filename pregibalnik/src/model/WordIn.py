from pydantic import BaseModel, constr


class WordIn(BaseModel):
    lema: constr(min_length=1)
    msd: constr(min_length=1)
