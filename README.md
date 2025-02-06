# Backstage Simple Client

A simple client for the [Backstage](https://backstage.io/) developer portal.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)

## Installation

To install the Backstage Simple Client, you can use `pip`:

```sh
pip install backstage-simple-client
```

## Usage

Here's an example of how to use the Backstage Simple Client:

```python
from backstage_simple_client.client import BackstageClient
from backstage_simple_client.filters import Filter, FullSearchFilter

# Initialize the client
base_url = "https://example.com"
token = "your-token-here"

with BackstageClient(base_url, token=token) as client:
    # Search entities with a filter
    entities = client.search_entities(
        filter=Filter(metadata_namespace='development')
    )

# Print the results
for entity in entities.items:
    print(entity.metadata.name)
```

## Examples

#### Multiple filters

```
entities = client.search_entities(
    filter = [
        Filter(kind='component', metadata_namespace='development'),
        Filter(kind='user')
    ]
)
```

#### Full-text search

```
entities = client.search_entities(
    full_text_filter = FullSearchFilter(term = "foobar", fields = ["metadata.name"])
)
```

#### Selecting fields, while applying limits and ordering

```
entities = client.search_entities(
    filter = Filter(kind='component', metadata_namespace='development'),
    fields = ['kind', 'metadata.name'],
    limit = 10,
    order_field = 'kind,asc'
)
```

#### Using pagination

```
pages = client.search_entities(
        filter   = Filter(kind='user')
        paginate = True
)
for page in pages:
    for entity in page.items:
        print(entity.metadata.name)
```

#### Getting entity by uid

```
entity = client.get_entities(uid="0442f73b-c3e9-4a94-a790-0981809b7267")
```

#### Getting entity (with its ancestry) by name 

```
entity = client.get_entities(kind="User", name="jdoe")
entities = client.get_entities(kind="User", name="jdoe", ancestry=True)
```

#### Geting entities by refs
        
```
entities = client.get_entities(refs=["user:default/jdoe", "user:default/gijoe"], fields=["metadata.name", "metadata.namespace", "metadata.uid"])
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request on GitHub.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.