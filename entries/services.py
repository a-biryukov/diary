from django.contrib.postgres.search import SearchQuery, SearchVector


def search_by_title_abd_text(queryset, query, user) -> list:
    """ Осуществляет поиск по запросу пользователя в полях 'title' и 'text' """
    query = SearchQuery(query)
    search_vector = SearchVector('title', 'text')
    queryset = queryset.annotate(search=search_vector).filter(owner=user, search=query)
    return queryset
