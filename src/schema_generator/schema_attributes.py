from typing import List, Type, TypeVar
import types
from .utils import get_inner
from .t import T
import re


class SchemaAttributes:
    """
    Used to define the attributes of a set of schemas.
    ALL: List[Type] = All the attributes of the class
    ENTITIES: List[Type] = All the attributes that are entities (have a bound that is a string)
    """
    ALL: List[Type] = []
    ENTITIES: List[Type] = []

    def __init_subclass__(cls) -> None:
        """
        When initiating a subclass, it will register all the attributes of the class.
        """
        attributes = []
        entities = []
        for name, value in cls.__dict__.items():
            #Ignore private attributes & classes
            if not name.startswith("__") and not name.endswith("__") and not isinstance(value, (type, types.ClassMethodDescriptorType)):
                if isinstance(value, T):
                    setattr(cls, name, TypeVar(f"{name}", bound=value.type))
                    value = getattr(cls, name)
                attributes.append(value)
                if hasattr(value, "__bound__") and isinstance(get_inner(value.__bound__), str):
                    entities.append(value)

        setattr(cls, "ALL", attributes)
        setattr(cls, "ENTITIES", entities)


    class Config:
        """
        Allow to define a mapping for dynamic schemas, for example:\n
        If you have a schema to read ALL the attributes of a User and this user has a Team,
        you will also want to read attributes of the Team but not ALL attributes to avoid infinite recursion.

        Then you can define a mapping like this:\n
        mapping = {
            "ReadAll": "Read"
        }\n
        In this example, the schema for the team inside the schema UserReadAll will be TeamRead (instead of TeamReadAll)\n

        You can also add mapping for specific attributes, for example:\n
        team = {
            "Patch": "Create"
        }\n
        In this example, the schema for the team inside the schema UserPatch will be TeamCreate (instead of TeamPatch)\n
        """

        @classmethod
        def apply_default_mapping(cls, method_name):
            for pattern, replacement in cls.default_mapping.items():
                regex_pattern = re.compile(pattern.replace("*", ".*"))
                if regex_pattern.match(method_name):
                    return replacement
            return method_name

        default_mapping = {}
        mapping = {}
