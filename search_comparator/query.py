"""Query object
"""
class Query:
    """Query object
    """
    def __init__(self, query: str, weighting: float=None, 
        tags: list = []):
        """This is a query object.
        Params:
            query: The query itself 
            weighting: how much weighting to put on the query. Shoud be float value. 1 is unit.
            tags: what is this query associated with
        """
        self.query = query
        self.tags = tags
        self.weighting = weighting

    def __str__(self):
        return self.query
