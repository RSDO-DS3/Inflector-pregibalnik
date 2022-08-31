from pydantic import BaseModel


class OrthographyOut(BaseModel):
    text: str
    morphologyPatterns: str
