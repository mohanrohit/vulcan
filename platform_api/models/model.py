from datetime import datetime

from pydantic import BaseModel
from pydantic import ConfigDict


class Model(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    def dict(self, **kwargs):
        return super().model_dump(mode="json", **kwargs)
