from typing import List, Union, Type, TypeVar
import re

def one_of(*attributes: List[Union[str, Type[TypeVar]]]):
    final_attributes = []
    for attr in attributes:
        if isinstance(attr, TypeVar):
            final_attributes.append(attr.__name__)
            continue
        final_attributes.append(attr)

    def verifier(value, values, field, cls):
        for attr in final_attributes:
            if attr in values:
                return value
        raise Exception("You must specify one of these attributes: " + ", ".join(final_attributes) + " for " + cls.__name__ + " ! (Values: " + str(values) + ")")

    return verifier

def email():
    def verifier(value, values, field, cls):
        if value and not re.match("^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$", value):
            raise Exception("The field " + field + " must be an email !")
        return value
    return verifier