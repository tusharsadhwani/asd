def resolve_type(obj):
    """Given a json-like object, returns the schema for that object."""
    if isinstance(obj, list):
        return [resolve_type(i) for i in obj]

    elif isinstance(obj, dict):
        return {k: resolve_type(v) for k, v in obj.items()}

    else:
        return type(obj)
