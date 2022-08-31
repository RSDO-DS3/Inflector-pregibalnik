from pydantic import BaseModel, constr


class FormIn(BaseModel):
    text: constr(min_length=1)
    msd: constr(min_length=1)
