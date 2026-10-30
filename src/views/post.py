from pydantic import BaseModel, AwareDatatime


class PostOut(BaseModel):
    id: int
    title: str
    content: str
    published_at: AwareDatatime | None
