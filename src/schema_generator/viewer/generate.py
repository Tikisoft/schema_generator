from ..utils import is_list, get_inner, is_forward
from ..base_schema import BaseSchema
import codecs
from enum import Enum
from pydantic import BaseModel
from .template import TEMPLATE

def block(name, content, template = None):
    if template == None:
        template = TEMPLATE
    return template.replace("{{" + name + "}}", content)


def generate_html(*schemas, path="generated.html"):
    nav = ""
    body = "<div class='flex flex-col pb-10'>"
    names = {}
    other_schemas = []
    enums = []
    for schema in schemas:
        if(issubclass(schema, BaseSchema)):
            if schema._name not in names:
                names[schema._name] = [schema]
            else:
                names[schema._name].append(schema)
        else:
            other_schemas.append(schema)

        for f in schema.__fields__:
            if not is_forward(schema.__fields__[f].type_) and issubclass(schema.__fields__[f].type_, Enum):
                enum = schema.__fields__[f].type_
                if enum not in enums:
                    enums.append(enum)

    for name in names:
        nav += nav_category(name, "nav-"+name, [nav_item(schema._name+schema._method, schema._name+schema._method) for schema in names[name]])
        body += section(name, full=True, class_="mt-20" if name != next(iter(names)) else "mt-10", children=[f"<span class='text-sm text-gray-500'>{len(names[name])} schema(s)</span>"])
        for schema in names[name]:
            body += schema_card(schema)

    if other_schemas:
        nav += nav_category("Pydantic Schemas", "nav-pydantic", [nav_item(schema.__name__, schema.__name__) for schema in other_schemas])
        body += section("Pydantic Schemas", full=True, class_="mt-20", children=[f"<span class='text-sm text-gray-500'>{len(other_schemas)} schema(s)</span>"])
        for schema in other_schemas:
            body += schema_card(schema)

    if enums:
        nav += nav_category("Enums", "nav-enums", [nav_item(enum.__name__, enum.__name__) for enum in enums])
        body += section("Enums", full=True, class_="mt-20", children=[f"<span class='text-sm text-gray-500'>{len(enums)} enum(s)</span>"])
        for enum in enums:
            body += enum_card(enum)
        
    body += "</div>"

    save_html(block("nav", nav, block("body", body)), path)

def save_html(html, path):
    f = codecs.open(path, "w", "utf-8")
    f.write(html)
    f.close()

def section(name, id="section", full=False, class_="", children=[], inner=None):
    content = f"<div id='{id}' class='shadow-lg rounded-lg border-2 border-gray-200 {'w-5/6' if full else 'w-4/5 md:w-3/4 lg:w-2/3 xl:w-1/2'} mx-auto {class_}'><div class='{'border-b-2 border-gray-200 rounded-t-lg' if inner else 'rounded-lg'} bg-white px-4 py-5 sm:px-6 flex justify-between items-center'><h3 class='text-lg font-medium leading-6 text-gray-900'>{name}</h3>{' '.join(children)}</div>"
    content += ("<div class='py-4'>" + inner + "</div>" if inner else "") + "</div>"
    return content

def schema_card(schema):
    color, nuance = "gray", 300

    name = schema.__name__
    method = ""
    if issubclass(schema, BaseSchema):
        name = schema._name
        method = schema._method
        if schema._method.startswith("Read"):
            color, nuance = "blue", 400
        if schema._method.startswith("Patch"):
            color, nuance = "yellow", 400
        if schema._method.startswith("Create"):
            color, nuance = "green", 400
        if schema._method.startswith("Delete"):
            color, nuance = "red", 400
        
    content = "<ul>"

    for f in schema.__fields__:
        props = schema.__fields__[f]
        is_entity = is_forward(props.type_) or issubclass(props.type_, BaseModel)
        is_enum = not is_entity and issubclass(props.type_, Enum)
        attr = props.name
        if props.required:
            attr += "<span class='text-red-500'>*</span>"
        attr += ": "
        if is_entity or is_enum:
            if is_forward(props.type_):
                href = get_inner(props.type_)
            else:
                href = props.type_.__name__
            attr += f"<a class='font-medium' href='#{href}'> {href}</a>" + (" (enum)" if is_enum else "")
        else:
            attr += props.type_.__name__

        type_ = props.outer_type_ if not hasattr(props.outer_type_, "__bound__") else props.outer_type_.__bound__
        if is_list(type_):
            attr += "[]"
        content += f"<li class='ml-4'>{attr}</li>"
    content += "</ul>"
    
    return section(name+method, name+method, class_="mt-10", children=[badge(method if method != "" else "Schema", color, nuance)], inner=content)

def enum_card(enum: Enum):
    return section(enum.__name__, enum.__name__, class_="mt-10", children=[badge("Enum", "purple", 400)],
        inner="<ul>" + "".join([f"<li class='ml-4'>{member.name} → {member.value}</li>" for member in enum]) + "</ul>")

def nav_category(name, id, items):
    content = f"""<div class="space-y-1">
                  <button type="button" class="bg-white text-gray-600 hover:bg-gray-100 w-full flex items-center pr-2 py-2 text-left text-sm font-medium rounded-md" data-submenu="{id}">
                    <svg sidebar-toggle-item class="text-gray-300 w-6 h-6 mr-2 transition-all -rotate-90" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd"></path></svg>
                    {name}
                  </button>
                  <div class="space-y-1" id="{id}">
                    {"".join(items)}
                  </div>
                </div>"""
    return content

def nav_item(name, href):
    return '<a href="#' + href +'" class="flex w-full items-center rounded-md py-2 pl-10 pr-2 text-sm font-medium text-gray-600 hover:bg-gray-100">' + name + '</a>'

def badge(text, color="gray", nuance=200):
    return f"<span class='hidden md:block text-md text-white py-1 px-3 leading-6 text-gray-900 bg-{color}-{nuance} border-2 border-{color}-{nuance+100} rounded-lg font-medium'>{text}</span>"