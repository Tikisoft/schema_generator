from ..utils import get_inner, is_forward
from ..base_schema import BaseSchema
import codecs
from enum import Enum
from pydantic import BaseModel
from datetime import datetime
import os

all_schemas = []

def convert_files(*schemas, path="generated"):
    names = {}
    other_schemas = []
    enums = []
    for schema in schemas:
        if(issubclass(schema, BaseSchema)):
            if schema._method.startswith("Read"):
                continue
            if schema._name not in names:
                names[schema._name] = [schema]
            else:
                names[schema._name].append(schema)
        else:
            other_schemas.append(schema)
        all_schemas.append(schema)

        for f in schema.__fields__:
            if not is_forward(schema.__fields__[f].type_) and issubclass(schema.__fields__[f].type_, Enum):
                enum = schema.__fields__[f].type_
                if enum not in enums:
                    enums.append(enum)

    for name in names:
        try:
            os.mkdir("src/converter/generated/" + name)
        except:
            pass
        for schema in names[name]:
            save_file(get_schema(schema), path, name, name + "/" + schema._name + schema._method)

    if other_schemas:
        for schema in other_schemas:
            save_file(get_schema(schema), path, None, schema.__name__)

    """if enums:
        for enum in enums:
            body += enum_card(enum)"""
    

def save_file(code, base_path, category, path):
    if base_path.endswith("/"):
            base_path = base_path[:-1]

    if not os.path.exists(base_path):
        raise FileNotFoundError(f"Can' found specified path: {base_path}")
    if category and not os.path.exists(base_path+"/"+category):
        os.mkdir(base_path+"/"+category)

    f = codecs.open(f"{base_path}/{path}.ts", "w", "utf-8")
    f.write(code)
    f.close()

def get_path(schema):
    if(not isinstance(schema, str) and issubclass(schema, BaseSchema)):
        return f"{schema._name}/{schema._name}{schema._method}"
    return schema if isinstance(schema, str) else schema.__name__

def find_shema(name):
    for schema in all_schemas:
        if schema.__name__ == name:
            return schema

def get_schema(schema):
    imported = []
    imports = ""

    definition = "export interface " + schema.__name__ + " {\n"
    for f in schema.__fields__:
        props = schema.__fields__[f]
        definition += f"    {props.name}{'?' if not props.required else ''}: "
        is_entity = is_forward(props.type_) or issubclass(props.type_, BaseModel)
        is_enum = not is_entity and issubclass(props.type_, Enum)
        is_forward_ = is_forward(props.type_)
        if is_entity:
            definition += get_inner(props.type_).__name__ if not is_forward_ else get_inner(props.type_)
            relation = get_inner(props.type_)
            if relation not in imported:
                imported.append(relation)
                imports += "import { " + (relation if is_forward_ else relation.__name__) + " } from '" + (".." if not is_forward_ and issubclass(get_inner(props.type_), BaseSchema) else ".") + "/" + get_path(relation) + "';\n"
        elif is_enum:
            definition += "|".join(["'"+member.name+"'" for member in props.type_])
        else:
            if issubclass(props.type_, bool):
                definition += "boolean"
            elif issubclass(props.type_, datetime):
                definition += "Date"
            elif issubclass(props.type_, (int, float)):
                definition += "number"
            elif issubclass(props.type_, str):
                definition += "string"
            
        definition += ",\n"
    definition += "}"

    content = imports + "\n" + definition

    return content