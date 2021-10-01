"""Evaluator for better search.
"""
import json
import pandas as pd
import numpy as np
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

    def evaluate(self, refresh=False):
        """For new queries or new models - it will re-evaluate
        """
        self._recorder.record_results(self.queries, self.searches, refresh=refresh)
        # Now you want to evaluate the RBO score of each result
        print("You can now compare across the different search results. Run show comparisons.")
    
    def get_query_result(self, query):
        return self._recorder.get_query_result(query)

    def show_all_results(self):
        show_results = defaultdict(dict)
        for q in self._recorder.recorder:
            for s in self._recorder.recorder[q]:
                show_results[q][s] = self._recorder.recorder[q][s]._inner_list
        return show_results

    def evaluate_query_result(self, query):
        """Scores the query results"""
        print(query)
        model_results = self._recorder.get_query_result(query)
        scores = defaultdict(dict)
        for i, (model_name, r) in enumerate(model_results.items()):
            for j, (model_name_2, r_2) in enumerate(model_results.items()):
                if i == j:
                    scores[model_name][model_name_2] = np.nan
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
    
    def list_queries(self):
        return self._queries
    
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
    
    def list_searches(self):
        return list(self._searches)
    
    def add_search(self, search: Callable, name: str=None, search_metadata={}):
        """here, we have the search configuration for ensuring that the search
        is useful.
        """
        self._searches[name] = search

    def plot_comparisons_by_query(self, query, return_as_dataframe=False, cmap="Blues"):
        results = self.evaluate_query_result(query)
        if return_as_dataframe:
            return pd.DataFrame(results)
        for q in results:
            for s in results[q]:
                results[q][s] = round(results[q][s][0], 3)
        # for c in df.columns:
        #     df[c] = df[c].apply(lambda x: x[0] if not pd.isna(x) else 0)
        df = pd.DataFrame(results)
        return df.style.background_gradient(cmap=cmap, high=1, low=0, axis=None)
    
    def plot_all_results_for_search(self, search_config_name: str, cmap="Blues", high=1, low=0, 
        axis=None, return_as_json: bool=True):
        scores = defaultdict(dict)
        for q in self.queries:
            for q_2 in self.queries:
                query_results = self._recorder.get_query_result(q)
                query_results_2 = self._recorder.get_query_result(q_2)
                scores[q][q_2] = self.score(
                    query_results[search_config_name].to_ids(),
                    query_results_2[search_config_name].to_ids()
                )[0]
        if return_as_json:
            return scores
        df = pd.DataFrame(scores)
        return df.style.background_gradient(cmap=cmap, high=high, low=low, axis=axis)

    def _add_fn_extension(self, filename):
        if not filename.endswith(".json"):
            filename = filename + ".json" 
        return filename

    def save(self, filename):
        filename = self._add_fn_extension(filename)
        with open(filename, 'w') as f:
            json.dump(self._recorder.to_json(), f)
        print(f"saved to {filename}")
        
    def load(self, filename):
        filename = self._add_fn_extension(filename)
        with open(filename, 'r') as f:
            d = json.load(f)
        self._recorder = ResultsRecorder()
        self._recorder.from_json(d)
    
    def compare_results(self, query_example: str, field: str=None, return_as_json=False):
        """Compare the results of a Pandas DataFrame
        """
        results_to_compare = {}
        for search_name, result_list in self._recorder._recorder[query_example].items():
            if field is None:
                results_to_compare[search_name] = result_list.to_list()
            else:
                results_to_compare[search_name] = [r.get(field) for r in result_list.to_list()]    
        if return_as_json:
            return results_to_compare
        return pd.DataFrame(results_to_compare)

    def compare_two_searches(self, search_config_1: str, 
        search_config_2: str, return_as_json: bool=False, cmap: str="Blues",
        high: float=1, low: float=0, axis=None):
        scores = defaultdict(dict)
        for q in self.queries:
            for q_2 in self.queries:
                query_results = self._recorder.get_query_result(q)
                query_results_2 = self._recorder.get_query_result(q_2)
                scores[q][q_2] = self.score(
                    query_results[search_config_1].to_ids(),
                    query_results_2[search_config_2].to_ids()
                )[0]
        if return_as_json:
            return scores
        df = pd.DataFrame(scores)
        return df.style.background_gradient(cmap=cmap, high=high, low=low, axis=axis)

    def show_json_compare_results(self, query_example: str, *args, **kwargs):
        from jsonshower import show_json
        return show_json(self.compare_results(query_example, return_as_json=True), *args, **kwargs)
