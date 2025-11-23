from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_snake
from pydantic_extra_types.color import Color


class Embed(BaseModel):
    id: str
    createdAt: datetime
    title: Optional[str] = None
    author: Optional[str] = None
    description: Optional[str] = None
    image: Optional[str] = None
    isImageThumbnail: bool
    color: Optional[Color] = None

    model_config = ConfigDict(
        validate_by_alias=False, serialize_by_alias=False, alias_generator=to_snake
    )
