# Search Comparator

This creates a search comparator object to help you compare searches that are written.

# Installation 

Install via pip:

```
pip install search-comparator
```

# How To Use 

```{python}

from search_comparator import Comparator

def search_option_1(query):
    return ['a', 'b', 'c']

def search_option_2(query):
    return ['d', 'b', 'a']

def search_option_3(query):
    return ['g', 'a', 'c']

queries = [
    "query_example_1",
    "query_example_2"
]

comparator = Comparator()
comparator.add_queries(queries)
comparator.add_search(search_option_1, "sample_search_1")
comparator.add_search(search_option_2, "sample_search_2")
comparator.add_search(search_option_3, "sample_search_3")

comparator.evaluate()
comparator.show_comparisons(queries[0])

```

![image](example.png)

You can then also see all the results using: 
```
comparator.show_all_results()
```

When creating a search comparator, it is reliant on there being a standardised results format.
It must either be a list of strings or a list of dictionaries with an _id available attached.
This can be customised. 

The purpose of this is to identify when searches are similar or different based on specific queries and models when
researched on mass.

In the future - there will be better support for differente evaluations.
