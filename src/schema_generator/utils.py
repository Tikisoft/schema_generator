from typing import Union

def get_inner(type_, max=None):

    if max == 0:
        return type_

    if is_optional(type_) or is_list(type_):
        return get_inner(type_.__args__[0], max=max-1 if max else None)

    if is_union(type_):
        return [get_inner(arg) for arg in type_.__args__]

    if is_forward(type_):
        return get_inner(type_.__forward_arg__, max=max-1 if max else None)

    return type_

def is_union(type_, recursive=False):
    res = (
        hasattr(type_, "__origin__")
        and type_.__origin__ == Union
        and not is_optional(type_, recursive)
    )
    if not recursive or isinstance(type_, str) or res:
        return res
    inner = get_inner(type_, 1)
    if inner == type_:
        return False
    return is_union(inner, recursive=recursive)

def is_optional(type_, recursive=False):
    res = False
    if hasattr(type_, "__origin__") and type_.__origin__ == Union:
        if len(type_.__args__) == 2:
            for arg in type_.__args__:
                if arg == type(None):
                    res = True
    if not recursive or isinstance(type_, str) or res:
        return res
    inner = get_inner(type_, 1)
    if inner == type_:
        return False
    return is_optional(inner, recursive=recursive)

def is_list(type_, recursive=False):
    res = (
        hasattr(type_, "__origin__")
        and type_.__origin__ == list
    )
    if not recursive or isinstance(type_, str) or res:
        return res
    inner = get_inner(type_, 1)
    if inner == type_:
        return False
    return is_list(inner, recursive=recursive)

def is_forward(type_, recursive=False):
    res = (
        hasattr(type_, "__forward_arg__")
    )
    if not recursive or isinstance(type_, str) or res:
        return res
    inner = get_inner(type_, 1)
    if inner == type_:
        return False
    return is_forward(inner, recursive=recursive)