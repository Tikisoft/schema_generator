from schema_generator import BaseSchema
from schemas.user_schemas import UserSchemas
from schemas.post_schemas import PostSchemas
from schemas.location_schemas import LocationSchemas

BaseSchema.forward_all()
