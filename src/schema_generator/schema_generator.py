from pydantic import PrivateAttr
from typing import Optional, Type, TypeVar, List, Union
from .base_schema import BaseSchema
from .schema_attributes import SchemaAttributes
from .t import T
from sqlalchemy.orm import declarative_base

def Optional_(*fields: Union[T, List[Type], Type[BaseSchema]]) -> Optional[TypeVar]:
    """Turn fields into Optional fields"""
    if len(fields) == 0:
        return []
        
    new_fields = []
    for f in fields:
        #If 'f' is a schema
        if isinstance(f, type) and issubclass(f, BaseSchema):
            #We retrieve the fields of the schema and make them optional
            schema_fields = Optional_(*f.__fields)
            if isinstance(schema_fields, list):
                new_fields.extend(schema_fields)
            else:
                new_fields.append(schema_fields)
        
        elif isinstance(f, list):
            normal_fields = Optional_(*f)
            if isinstance(normal_fields, list):
                new_fields.extend(normal_fields)
            else:
                new_fields.append(normal_fields)
        else:
            new_fields.append(TypeVar(f"{f.__name__}", bound=Optional[f.__bound__]))

    if len(new_fields) == 1:
        return new_fields[0]
    return new_fields

#Alias for Optional_
O = Optional_

class Remove:
    """Remove fields from the schema"""
    def __init__(self, *fields: Union[T, List[Type], Type[BaseSchema]]) -> None:
        self.fields = fields

#Alias for Remove
R = Remove

class SchemaGenerator():

    def __init__(self, base_model: Type[declarative_base()], schema_attributes: Type[SchemaAttributes], name: str):
        """
        Create a new SchemaGenerator

        base_model: The SQLAlchemy model class to use
        schema_attributes: The SchemaAttributes class to use for the schemas generated
        name: The name of the schemas generated without any method (for example "User")
        """
        self.base_model = base_model
        self.schema_attributes = schema_attributes
        self.name = name

        self.schemas = {}
    
    def new_schema(self, method: str, *fields: Union[Remove, BaseSchema, T, List[Type], Type[BaseSchema], TypeVar], verifiers = {}) -> Type[BaseSchema]:

        Schema: Type[BaseSchema] = type(self.name+method, (BaseSchema,), {"_name": self.name, "_method": method, "_verifiers": verifiers, "_config_attributes": self.schema_attributes.Config, "_orm_model": PrivateAttr(self.base_model)})

        for field in fields:
            if not isinstance(field, R):
                Schema.add_fields(field)
            else:
                Schema.remove_fields(*field.fields)

        self.schemas[method] = Schema
        
        Schema.generate()
        return Schema

    def get_schema(self, method) -> Type[BaseSchema]:
        return self.schemas[method]