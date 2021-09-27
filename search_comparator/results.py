"""Building a result list
"""
from typing import List
from collections import defaultdict
import collections

def indexing_decorator(func):

    def decorated(self, index, *args):
        if index == 0:
            raise IndexError('Indices start from 1')
        elif index > 0:
            index -= 1

        return func(self, index, *args)

    return decorated


class ResultList(collections.MutableSequence):
    def __init__(self, original_list):
        self._inner_list = original_list

    def __len__(self):
        return len(self._inner_list)

    @indexing_decorator
    def __delitem__(self, index):
        self._inner_list.__delitem__(index)

    @indexing_decorator
    def insert(self, index, value):
        self._inner_list.insert(index, value)

    @indexing_decorator
    def __setitem__(self, index, value):
        self._inner_list.__setitem__(index, value)

    @indexing_decorator
    def __getitem__(self, index):
        return self._inner_list.__getitem__(index)

    def append(self, value):
        self.insert(len(self) + 1, value)

    def _get_result_ids(self, result_list: list) -> List:
        """Return a list of result IDs
        """
        if isinstance(result_list[0], dict):
            result_list = [r['_id'] for r in result_list]
        return result_list

    def to_ids(self):
        if isinstance(self._inner_list[0], dict):
            return self._get_result_ids(self._inner_list)
        return self._inner_list
    
    def to_list(self):
        return self._inner_list

# class ResultList(list):
#     def __init__(self, result_list: list):
#         """Get the required result list
#         """
#         if isinstance(result_list, dict) and 'results' in result_list:
#             result_list = result_list['results']
#         self.result_list = result_list
    
#     def __getitem__(self, key):
#         return super(ResultList, self).__getitem__(key - 1)

#     def _get_result_ids(self, result_list: list) -> List:
#         """Return a list of result IDs
#         """
#         if isinstance(result_list[0], dict):
#             result_list = [r['_id'] for r in result_list]
#         return result_list

#     def to_ids(self):
#         return self._get_result_ids(self.result_list)

    # def _clean_result_list(self, result_list):
    #     self.clean_result_list = self._get_result_ids(result_list)

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
    _recorder = defaultdict(dict)
    
    @property
    def recorder(self):
        return self._recorder

    def record_results(self, queries, searches, refresh=False):
        """Record all the results
        """
        for q in queries:
            for search_name, search in searches.items():
                if refresh or search_name not in self.recorder[q]:
                    results = ResultList(search(q))
                    self._recorder[q][search_name] = results

    def get_query_result(self, query):
        return self.recorder[query]
    
    def to_json(self):
        """To JSON file
        """
        results_list_all = defaultdict(dict)
        for query, search_config in self._recorder.items():
            for search_config, results_list in search_config.items():
                results_list_all[query][search_config] = results_list.to_list()
        return results_list_all

    def from_json(self, json_data):
        for q in json_data:
            for search_name, search in json_data[q].items():
                results = ResultList(search)
                self._recorder[q][search_name] = results
