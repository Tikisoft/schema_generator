from sqlalchemy_pydantic_orm import ORMBaseSchema
from pydantic.fields import ModelField
from typing import List, Optional, Dict, Type, TypeVar, TYPE_CHECKING, Union
from .utils import get_inner, is_list, is_optional

if TYPE_CHECKING:
    from schema_attributes import SchemaAttributes

REFS = {}

class BaseSchema(ORMBaseSchema):

    #Fields of the schema, for example [User.id, User.name]
    __fields = []
    #Name of the schema, for example "User"
    _name: str = None
    #Method of the schema, for example "Read"
    _method: str = None
    #Config of the schema, it contains the maping of the attributes
    _config_attributes: "SchemaAttributes.Config" = None
    #Validators
    _verifiers: Dict = {}

    class Config:
        orm_mode = True
        use_enum_values = True

    def __init__(self, **data):
        for attr in self._verifiers:
            for verifier in self._verifiers[attr]:
                res = verifier(data[attr] if attr in data else None, data)
                if attr in data:
                    data[attr] = res

        super().__init__(**data)
                

    def __init_subclass__(cls) -> None:
        cls.add_fields = lambda *fields: BaseSchema.__add_fields(cls, *fields)
        cls.remove_fields = lambda *fields: BaseSchema.__remove_fields(cls, *fields)
        cls.generate = lambda: BaseSchema.__generate(cls)
        cls.get_field_type = lambda field: BaseSchema.__get_field_type(cls, field)

        if cls.__name__ not in REFS:
            REFS[cls.__name__] = cls
        return super().__init_subclass__()


    #Add fields to the schema
    @staticmethod   
    def __add_fields(cls: Type["BaseSchema"], *fields: List[Union["BaseSchema", Type]]):
        for field in fields:
            if isinstance(field, list):
                cls.__add_fields(cls, *field)
                continue
            if isinstance(field, type) and issubclass(field, BaseSchema):
                cls.__add_fields(cls, *getattr(field, "__fields", []))
                continue
            cls.__remove_fields(cls, field)
            setattr(cls, "__fields", [*getattr(cls, "__fields", []), field])

    #Remove fields from the schema
    @staticmethod
    def __remove_fields(cls: Type["BaseSchema"], *fields: List[Union["BaseSchema", Type]]):
        for field in fields:
            if isinstance(field, list):
                cls.__remove_fields(cls, *field)
                continue
            if isinstance(field, type) and issubclass(field, BaseSchema):
                cls.__remove_fields(cls, *getattr(field, "__fields", []))
                continue
            fields = getattr(cls, "__fields", [])
            for f in fields:
                if f.__name__ == field.__name__:
                    fields.remove(f)
                    break

            setattr(cls, "__fields", fields)

    #Generate the schema
    @staticmethod
    def __generate(cls: Type["BaseSchema"]):
        """
        Generate the fields and annotations of the schema.
        """
        
        cls.__fields__.clear()
        cls.__annotations__.clear()

        new_annotations: Dict[str, Optional[type]] = {}
        new_fields: Dict[str, ModelField] = {}

        for field in getattr(cls, "__fields", []):

            type_, type_name = cls.__get_field_type(cls, field)

            new_annotations[type_name] = type_
            new_fields[type_name] = ModelField(
                name=type_name,
                type_=new_annotations[type_name],
                class_validators=None,
                default=[] if is_list(type_) else None,
                model_config=cls.__config__,
            )

        cls.__fields__.update(new_fields)
        cls.__annotations__.update(new_annotations)

    @staticmethod
    def __get_field_type(cls, field: Type):
        """
        Get the type of a field.
        If the field is a TypeVar, it will return the bound of the TypeVar.
        If the field is bound to a string, it will determine the schema corresponding to the string and dependant on the current schema's method (Read/Create/...).
            For example, if we are in the UserCreate schema, and the field is bound to "Team", it will return the TeamCreate schema.
            For example, if we are in the UserReadAll schema, and the field is bound to "Team", it will return the TeamRead schema. (instead of TeamReadAll thanks to the mapping)
        """

        type_ = get_inner(field)
        type_name = type_.__name__ if hasattr(type_, "__name__") else type_

        if isinstance(get_inner(type_.__bound__), str):

            if hasattr(cls._config_attributes, type_name) and cls._method in getattr(cls._config_attributes, type_name):
                type_ = get_inner(type_.__bound__)+getattr(cls._config_attributes, type_name)[cls._method]
            elif cls._method in cls._config_attributes.mapping:
                type_ = get_inner(type_.__bound__)+cls._config_attributes.mapping[cls._method]
            else:
                type_ = get_inner(type_.__bound__)+cls._method

            if is_list(field.__bound__, True):
                type_ = List[type_]

            if is_optional(field.__bound__, True):
                type_ = Optional[type_]

            return TypeVar(f"{field.__name__}", bound=type_), type_name

        return field, type_name

    @staticmethod
    def forward_all():
        for _, cls in REFS.items():
            cls_refs = {}
            for field in cls.__fields__:
                annotation_type = get_inner(cls.__fields__[field].type_)
                if type(annotation_type) == str:
                    if annotation_type in REFS:
                        cls_refs[annotation_type] = REFS[annotation_type]
                    else:
                        print("Can't find reference of", annotation_type, "for attribute", field, "in", cls.__name__, "schema")
            if cls_refs:
                cls.update_forward_refs(**cls_refs)