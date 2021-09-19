"""Evaluator for better search.
"""
import pandas as pd
from collections import defaultdict
from typing import Union, Callable
from .query import Query
from .results import ResultList, ResultsRecorder
from .rbo import VDBRBOScorer

class Comparator:
    """Evaluating the RBO scores.
    """
    _queries = {}
    _searches = {}
    _recorder = ResultsRecorder()

    def __init__(self, score: Callable=None):
        """If you want to change the scorer to something else, you can. 
        By default, uses an RBO scorer. 
        Score accepts 2 lists and and then runs searches.
        """
        self.score = VDBRBOScorer().score_rbo if score is None else score

    def evaluate(self):
        """For new queries or new models - it will re-evaluate
        """
        self._recorder.record_results(self.queries, self.searches)
        # Now you want to evaluate the RBO score of each result
        print("You can now compare across the different search results. Run show comparisons.")
    
    def get_query_result(self, query):
        return self._recorder.get_query_result(query)

    def evaluate_query_result(self, query):
        """Scores the query results"""
        model_results = self._recorder.get_query_result(query)
        scores = defaultdict(dict)
        for i, (model_name, r) in enumerate(model_results.items()):
            for j, (model_name_2, r_2) in enumerate(model_results.items()):
                if i == j:
                    continue
                scores[model_name][model_name_2] = self.score(r.to_ids(), r_2.to_ids())
        return scores
    
    def evaluate_all_query_results(self):
        queries_all = defaultdict(dict)
        for query in self.queries.keys():
            queries_all[query] = self.evaluate_query_result(query)
        return queries_all

    def add_query(self, query: Union[str, Query]):
        """Add a query to an evaluated list.
        """
        if isinstance(query, str):
            query = Query(query)
        if query not in self._queries:
            self._queries[query] = []
    
    def add_queries(self, queries):
        [self.add_query(q) for q in queries]
    
    @property
    def queries(self):
        return [str(q) for q in self._queries.keys()]
    
    @queries.setter
    def queries(self, queries):
        return [self.add_query(q) for q in queries]
    
    def remove_query(self, query):
        self._queries.pop(query)

    @property
    def searches(self):
        return self._searches
    
    def remove_search(self, search_name: str):
        """Remove search by its name.
        """
        del self._searches[search_name]
    
    def add_search(self, search: Callable, name: str=None, search_metadata={}):
        """here, we have the search configuration for ensuring that the search
        is useful.
        """
        self._searches[name] = search

    def show_comparisons(self, query):
        return pd.DataFrame(self.evaluate_query_result(query))
    
    # def show_search_results(self):
    #     return {}