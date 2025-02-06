from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict

# Entities below were created to reflect as closely as possible the model described in the documentation
# https://backstage.io/docs/features/software-catalog/system-model

class EntityRelation(BaseModel):
    targetRef: str
    type: str

class EntityLink(BaseModel):
    url: str
    title: Optional[str] = None
    icon: Optional[str] = None
    type: Optional[str] = None

class EntityMetadata(BaseModel):
    name: str
    namespace: Optional[str] = None
    uid: Optional[str]
    title: Optional[str] = None
    description: Optional[str] = None
    labels: Optional[Dict[str, str]] = None
    annotations: Optional[Dict[str, Any]] = None
    tags: Optional[List[str]] = None
    links: Optional[List[EntityLink]] = None
    etag: Optional[str] = None

class EntitySpec(BaseModel):
    type: Optional[str] = None
    lifecycle: Optional[str] = None

    model_config = ConfigDict(extra='allow')

class Entity(BaseModel):
    apiVersion: str
    metadata: EntityMetadata
    spec: EntitySpec
    kind: str
    relations: Optional[List[EntityRelation]] = None