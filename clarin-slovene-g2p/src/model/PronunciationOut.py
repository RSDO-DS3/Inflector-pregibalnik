from pydantic import BaseModel


class PronunciationOut(BaseModel):
    text: str
    script: str
