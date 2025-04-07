from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    """Schéma de base avec configuration commune."""

    model_config = ConfigDict(from_attributes=True)
