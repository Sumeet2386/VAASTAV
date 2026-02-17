from pydantic import BaseModel

class VerifyResponse(BaseModel):
    status: str
    media_type: str
    confidence_score: int
