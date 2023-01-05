from schema_generator import generate_html, BaseSchema
from schemas import *

#Will generate an html file to visualize schemas
generate_html(*BaseSchema.__subclasses__(), path="examples/generated/viewer.html")