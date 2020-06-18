import unittest
import requests
from retrieve_definition import retrieve_definition


class TestWikiAPI(unittest.TestCase):

    def test_retrieve_definition(self):
        self.extract = retrieve_definition("cat")
        self.maxDiff = None
        self.assertEqual(len(self.extract), 300)
        


if __name__ == '__main__':
    unittest.main()
