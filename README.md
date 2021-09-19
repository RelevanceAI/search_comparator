# Search Comparator

This creates a search comparator object to help you compare searches that are written.

# How To Use 

```{python}
from search_comparator import Comparator

def search_option_1(query):
    return results

def search_option_2(query):
    return results 

queries = [
    "query_example_1",
    "query_example_2"
]

comparator = Comparator()
comparator.add_queries(queries)
comparator.add_search(search_option_1, "sample_search_1")
comparator.add_search(search_option_2, "sample_search_2")

comparator.evaluate()
comparator.show_different_searches()

```

When creating a search comparator, it is reliant on there being a standardised results format.
It must either be a list of strings or a list of dictionaries with an _id available attached.
This can be customised. 

The purpose of this is to identify when searches are similar or different based on specific queries and models when
researched on mass.

In the future - there will be better support for differente evaluations.
