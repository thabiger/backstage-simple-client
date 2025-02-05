from pydantic import BaseModel
from typing import List
from .entities import Entity

class PageInfo(BaseModel):
    nextCursor: str | None = None
    prevCursor: str | None = None

class QueryEntitiesResponse(BaseModel):
    items: List[Entity]
    totalItems: int
    pageInfo: PageInfo

class AncestryEntity(BaseModel):
    entity: Entity
    parentEntityRefs: List

class EntityAncestryResponse(BaseModel):
    rootEntityRef: str
    items: List[AncestryEntity]
    
class EntityList(BaseModel):
    items: List[Entity]