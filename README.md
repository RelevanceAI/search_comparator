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

def search_option_4(query):
    return [{"_id": "g"}, {"_id": "h"}, {"_id": "i"}]

queries = [
    "query_example_1",
    "query_example_2"
]

comparator = Comparator()
comparator.add_queries(queries)
comparator.add_search(search_option_1, "sample_search_1")
comparator.add_search(search_option_2, "sample_search_2")
comparator.add_search(search_option_3, "sample_search_3")
comparator.add_search(search_option_4, "sample_search_4")
comparator.evaluate()
df = comparator.show_comparisons("query_example_1", return_as_dataframe=True)
comparator.plot_comparisons_by_query("query_example_1")

```

![image](example.png)

You can then also see all the results using: 
```
comparator.show_all_results()
```

```
# You can also compare all the query results in order to help to explore relationships between search results
search_config_name = "use_search"
comparator.plot_all_results_for_search(search_config_name)
```

![image](query_analysis.png)

When creating a search comparator, it is reliant on there being a standardised results format.
It must either be a list of strings or a list of dictionaries with an _id available attached.
This can be customised. 

The purpose of this is to identify when searches are similar or different based on specific queries and models when
researched on mass.

```{python}
# Save
comparator.save("test")

# Load
comparator.load('test')

comparator.show_comparisons("query_example_1")

# Compare results for 1 query
comparator.compare_results(query)

```


In the future - there will be better support for differente evaluations.
