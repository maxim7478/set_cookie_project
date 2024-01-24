def to_dict_func(obj):
    d = {}
    for column in obj.__table__.columns:
        d[column.name] = str(getattr(obj, column.name))
    return d
