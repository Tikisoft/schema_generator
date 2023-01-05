from typing import Union

def get_inner(field, max=None):

    if max == 0:
        return field

    if is_optional(field) or is_list(field):
        return get_inner(field.__args__[0], max=max-1 if max else None)

    if is_forward(field):
        return get_inner(field.__forward_arg__, max=max-1 if max else None)

    return field

def is_optional(field, recursive=False):
    res = (
        hasattr(field, "__origin__")
        and field.__origin__ == Union
    )
    if not recursive or isinstance(field, str) or res:
        return res
    inner = get_inner(field, 1)
    if inner == field:
        return False
    return is_optional(inner, recursive=recursive)

def is_list(field, recursive=False):
    res = (
        hasattr(field, "__origin__")
        and field.__origin__ == list
    )
    if not recursive or isinstance(field, str) or res:
        return res
    inner = get_inner(field, 1)
    if inner == field:
        return False
    return is_list(inner, recursive=recursive)

def is_forward(field, recursive=False):
    res = (
        hasattr(field, "__forward_arg__")
    )
    if not recursive or isinstance(field, str) or res:
        return res
    inner = get_inner(field, 1)
    if inner == field:
        return False
    return is_forward(inner, recursive=recursive)