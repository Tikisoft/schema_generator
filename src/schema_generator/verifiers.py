from typing import List, Union, Type, TypeVar

def one_of(*attributes: List[Union[str, Type[TypeVar]]]):
    final_attributes = []
    for attr in attributes:
        if isinstance(attr, TypeVar):
            final_attributes.append(attr.__name__)
            continue
        final_attributes.append(attr)

    def verifier(value, values, cls):
        for attr in final_attributes:
            if attr in values:
                return value
        raise Exception("You must specify one of these attributes: " + ", ".join(final_attributes) + " for " + cls.__name__ + " ! (Values: " + str(values) + ")")

    return verifier