from typing import List

class Filter:
    def __init__(self, **kwargs):
        
        self.filter_map = {}

        for k, v in kwargs.items():
            self.filter_map[k.replace('_', '.')] = v

    def to_params(self):
        '''
            For such an input:
                {'kind': 'Component', 'namespace': 'development'}
            Returns:
                ('filter', 'kind=Component,namespace=development')
        '''
        return ('filter', ",".join(f"{k}={v}" for k, v in self.filter_map.items()))

class FullSearchFilter:
    def __init__(self, term: str, fields: List[str]):
        
        self.term = term
        self.fields = fields

    def to_params(self):
        return [
                ('fullTextFilterTerm', self.term),
                ('fullTextFilterFields', ",".join(self.fields))
                ]
