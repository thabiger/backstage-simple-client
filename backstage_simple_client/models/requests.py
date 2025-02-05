from pydantic import BaseModel, field_validator, model_validator
from typing import Any, Dict, List, Optional
from ..filters import Filter, FullSearchFilter

# test if provided values aren't breaking mutually exclusive groups
def test_mutually_exclusive(groups, values):
    for group in groups:
        present_args = group.intersection(values)
        if len(present_args) > 1:
            raise ValueError(f"Arguments {', '.join(present_args)} are mutually exclusive and cannot be used together.")

class SearchEntityQueryParams(BaseModel):
    filter: Optional[List[Filter]] = None
    full_text_filter: Optional[FullSearchFilter] = None
    fields: Optional[List[str]] = None
    limit: Optional[int] = None
    order_field: Optional[str] = None
    cursor: Optional[str] = None

    class Config:
        arbitrary_types_allowed=True

    @model_validator(mode="before")
    def check_mutually_exclusive(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        test_mutually_exclusive([
            {'filter', 'full_text_filter'},
            {'filters', 'full_text_filter'},
        ], values)

        return values

    @field_validator("filter", mode="before")
    def make_filter_list(cls, v):
        return [v] if isinstance(v, Filter) else v


class GetEntitiesRequestParams(BaseModel):
    uid: Optional[str] = None 
    kind: Optional[str] = None
    namespace: Optional[str] = "default"
    name: Optional[str] = None
    ancestry: Optional[bool] = False
    refs: Optional[List[str]] = None
    fields: Optional[List[str]] = None

    @model_validator(mode="before")
    def check_mutually_exclusive(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        test_mutually_exclusive([
            {'uid', 'name'},
            {'uid', 'refs'},
            {'name', 'refs'}
        ], values)

        return values