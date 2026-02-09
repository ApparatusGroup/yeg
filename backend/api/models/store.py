from pydantic import BaseModel, HttpUrl


class Store(BaseModel):
    id: str
    name: str
    domain: str
    homepage_url: HttpUrl
    platform: str | None = None
    neighborhood: str | None = None
    opted_out: bool = False
