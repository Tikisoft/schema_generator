from schema_generator import BaseSchema, convert_files
from schemas import *

#Will generate typescript classes
convert_files(*BaseSchema.__subclasses__(), path="examples/generated/typescript")