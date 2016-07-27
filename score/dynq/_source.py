import abc


class DataSource:

    def __init__(self):
        self.__name = None

    def handle_queries(self, ctx, queries):
        for query, mtime, autoupdate in queries:
            yield self.handle_query(ctx, query, mtime, autoupdate)

    def handle_query(self, ctx, query, mtime, autoupdate):
        outdated = self._is_outdated(ctx, query, mtime)
        if outdated is not None:
            if outdated:
                if not autoupdate:
                    return True
                new_mtime, result = self._query(ctx, query)
                return [new_mtime, list(result)]
            return False
        new_mtime, result = self._query(ctx, query)
        if new_mtime > mtime:
            if not autoupdate:
                return True
            return [new_mtime, list(result)]
        return False

    @property
    def name(self):
        if self.__name is None:
            self.__name = self.__class__.__name__
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    def _is_outdated(self, ctx, query, mtime):
        return None

    @abc.abstractmethod
    def _query(self, ctx, query):
        mtime = 0
        items = []
        return mtime, items
