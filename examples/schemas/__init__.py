from schema_generator import BaseSchema
from schemas.user_schemas import UserSchemas
from schemas.post_schemas import PostSchemas

BaseSchema.forward_all()
