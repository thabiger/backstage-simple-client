import unittest
import os
import re

from backstage_simple_client.client import BackstageClient
from backstage_simple_client.filters import Filter, FullSearchFilter

class TestBackstageClient(unittest.TestCase):

    def setUp(self):
        self.base_url = os.getenv("BACKSTAGE_BASE_URL")
        self.token = os.getenv("BACKSTAGE_TOKEN")
        self.client = BackstageClient(self.base_url, self.token)

    def test_search_entities_filter(self):

        entities = self.client.search_entities(
            filter = Filter(metadata_namespace='development')
        )

        # at least one entity of each kind is in the testing dataset, so no less than 2 entities should be returned        
        self.assertGreater(len(entities.items), 2)
        # only this kind of components should be returned
        self.assertEqual(set([e.metadata.namespace.lower() for e in entities.items]), set(["development"]))

    def test_search_entities_multiple_filter(self):

        entities = self.client.search_entities(
            filter = [Filter(kind='component', metadata_namespace='development'),
                Filter(kind='user')]
        )

        # at least one entity of each kind is in the testing dataset, so no less than 2 entities should be returned        
        self.assertGreater(len(entities.items), 2)
        # only this kind of components should be returned
        self.assertEqual(set([e.kind.lower() for e in entities.items]), set(["component", "user"]))

    def test_search_entities_limits_and_filters(self):

        entities = self.client.search_entities(
            filter = Filter(kind='component', metadata_namespace='development'),
            #fields = ['apiVersion', 'kind'],
            limit = 1
        )

        self.assertEqual(len(entities.items), 1)
        self.assertNotEqual(entities.items[0].apiVersion, "")
        self.assertNotEqual(entities.items[0].kind, "")
        #TODO: filtering not implemented at the moment
        #self.assertIsNone(entities.items[0].metadata)

    def test_search_entities_order_field(self):

        entities = self.client.search_entities(
            filter = Filter(kind='component', metadata_namespace='development'),
            order_field = 'metadata.name,asc'
        )

        entity_names = [ entity.metadata.name.lower() for entity in entities.items ]
        entity_names_sorted = sorted(entity_names)

        self.assertEqual(entity_names, entity_names_sorted)

    def test_search_entities_full_search(self):

        entities = self.client.search_entities(
            full_text_filter = FullSearchFilter(term = "service", fields = ["metadata.name"])
        )

        for name in [ entity.metadata.name.lower() for entity in entities.items ]:
            self.assertTrue(re.search("service", name))


    def test_search_mutually_exclusive(self):

        with self.assertRaises(ValueError):
            self.client.search_entities(
                full_text_filter = FullSearchFilter(term = "service", fields = ["metadata.name"]),
                filter = Filter(kind='component', metadata_namespace='development'),
            )
            
    def tearDown(self):
        self.client.close()

if __name__ == '__main__':
    unittest.main()
