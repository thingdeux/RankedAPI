def add_limit_and_offset_to_queryset(queryset, **kwargs):
    limit = kwargs.get('limit', None)
    offset = kwargs.get('offset', None)

    if limit and offset:
        queryset = queryset[int(offset):]
        queryset = queryset[:int(limit)]
    elif limit:
        queryset = queryset[:int(limit)]
    elif offset:
        queryset = queryset[int(offset):]
    return queryset