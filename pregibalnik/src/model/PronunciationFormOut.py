from pydantic import BaseModel


class PronunciationFormOut(BaseModel):
    text: str
    script: str
