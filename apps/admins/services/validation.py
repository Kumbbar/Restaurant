from core.exceptions import BadQueryParams


def validate_query_data(query_param: str):
    try:
        query_list = query_param.split(',')
        if not query_list:
            raise BadQueryParams('No values selected')
        return [int(id) for id in query_list]
    except ValueError:
        raise BadQueryParams('Invalid param')
