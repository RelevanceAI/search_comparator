"""Building a result list
"""
from typing import List
from collections import defaultdict

class ResultList(list):
    def __init__(self, result_list: list):
        """Get the required result list
        """
        if isinstance(result_list, dict) and 'results' in result_list:
            result_list = result_list['results']
        self.result_list = result_list
    
    def __getitem__(self, key):
        return super(ResultList, self).__getitem__(key - 1)

    def _get_result_ids(self, result_list: list) -> List:
        """Return a list of result IDs
        """
        if isinstance(result_list[0], dict):
            result_list = [r['_id'] for r in result_list]
        return result_list

    def to_ids(self):
        return self._get_result_ids(self.result_list)

    def _clean_result_list(self, result_list):
        self.clean_result_list = self._get_result_ids(result_list)

class ResultsRecorder:
    """
    Record the results.
    Stores it in the following format:
    {
        "query": {
            "search_name": [
                {"_id": "a"},
                {"_id": "b"},
                {"_id": "c"}
            ]
        },
        "query_2": {
            "search_name-2": [
                {"_id": "a"},
                {"_id": "b"},
                {"_id": "c"}
            ]
        }
    }
    """
    recorder: defaultdict = defaultdict(dict)
    def record_results(self, queries, searches, refresh=False):
        """Record all the results
        """
        for q in queries:
            for search_name, search in searches.items():
                if refresh or search_name not in self.recorder[q]:
                    self.recorder[q][search_name] = ResultList(search(q))

    def get_query_result(self, query):
        return self.recorder[query]
