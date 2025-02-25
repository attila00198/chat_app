from pydantic import BaseModel
from typing import Optional, Union


class Message(BaseModel):
    """Message model for handling messages"""

    type: str
    sender: str
    content: Union[str, list[str]]
    target: Optional[str] = None
