import httpx
import pydantic
from functools import wraps
from typing import Optional, Any, Dict, Callable, Any

from .models.entities import Entity
from .models.responses import QueryEntitiesResponse, EntityList, EntityAncestryResponse
from .models.requests import SearchEntityQueryParams, GetEntitiesRequestParams

from .common import *

def paginate(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        # this internal function is required here to prevent
        # wrapper function becoming a generator
        def gen(*args, **kwargs):
            cursor = None
            while True:
                if cursor:
                    kwargs['cursor'] = cursor
                response = func(*args, **kwargs)
                yield response
                cursor = response.pageInfo.nextCursor
                if not cursor:
                    break

        paginate = kwargs.pop('paginate', False)
        if not paginate:
            # If pagination is not requested, call the function normally
            return func(*args, **kwargs)
        else:
            # If pagination is requested, return a generator
            return gen(*args, **kwargs)

    return wrapper

def try_return(types, t=0, **r):
    # try to fit the data into passed models/types

    if not isinstance(types, list):
        types = [types]

    try:
        return types[t](**r)
    except pydantic.ValidationError as e:
        return try_return(types, t+1, **r)
    except IndexError:
        # Don't have an idea how to handle this response, gonna return it as is
        return r


class BackstageClient:

    def __init__(self, base_url: str, token: Optional[str] = None, timeout: float = 30.0):
        """
        :param base_url: The base URL of the Backstage instance, e.g. 'https://backstage.example.com'.
        :param token: Optional authentication token (if your Backstage is secured).
        :param timeout: Default timeout for HTTP requests (in seconds).
        """
        self.base_url = base_url.rstrip("/")
        self.token = token
        self.timeout = timeout

        # Create a reusable httpx client with optional token-based auth.
        headers = {}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"

        self._client = httpx.Client(
            base_url=self.base_url,
            headers=headers,
            timeout=self.timeout,
            verify=False
        )

    @paginate
    def search_entities(self, **kwargs) -> QueryEntitiesResponse:
        """
        Method for searching entities using /entities/by-query endpoint.
        
        :kwargs: query parameter dict, according to the
             https://backstage.io/docs/features/software-catalog/software-catalog-api/#entities
        :return: List of QueryEntitiesResponse objects.
        """
        url = "/api/catalog/entities/by-query?"

        def switch(key, v):
            switch = {
                'filter': 
                    lambda v: [ f.to_params() for f in v ],
                'fields': 
                    lambda v: ('fields', ",".join(v)),
                'limit': 
                    lambda v: ('limit', v),
                'order_field': 
                    lambda v: ('orderField', v),
                'full_text_filter': 
                    lambda v: v.to_params(),
                'cursor': 
                    lambda v: ('cursor', v)
            }
            return switch.get(key, lambda: "Default case")(v)
        
        params = flatten([ switch(k,v) for k,v in SearchEntityQueryParams(**kwargs).model_dump().items() if v ])

        response = self._client.get(url, params=params)
        response.raise_for_status()

        r = response.json()
        return try_return(QueryEntitiesResponse, **r)

    def get_entities(self, **kwargs) -> Entity | EntityList | EntityAncestryResponse:
        
        args = GetEntitiesRequestParams(**kwargs)

        args.fields = args.fields if args.fields else []
        ancestry_path = "/ancestry" if args.ancestry else ""
        
        endpoints: Dict[str, Any] = {
            "uid": {
                "name": "uid",
                "url": f"/api/catalog/entities/by-uid/{args.uid}",
                "method": "get",
            },
            "name": {
                "name": "name",
                "url": f"/api/catalog/entities/by-name/{args.kind}/{args.namespace}/{args.name}{ancestry_path}",
                "method": "get",
            },
            "refs": {
                "name": "refs",
                "url": "/api/catalog/entities/by-refs",
                "method": "post",
                "json": {
                    "entityRefs": args.refs,
                    "fields": args.fields
                }
            }
        }

        # pick the endpoint based on the parameters passed
        pick_endpoint = lambda _args, _endpoints: [x for x in _endpoints if _args.get(x) ]
        endpoint_name = pick_endpoint(args.model_dump(), endpoints.keys()).pop()
        endpoint = endpoints[endpoint_name]

        # use the content of json or params if available to make the request
        params = { k:v for k,v in endpoint.items() if k in ["json", "params"] }

        response = getattr(self._client, endpoint.get("method"))(url = endpoint.get("url"), **params)
        response.raise_for_status()
        r = response.json()

        return try_return([Entity, EntityList, EntityAncestryResponse], **r)

    def close(self):
        """Close the underlying HTTP session."""
        self._client.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
