from datetime import datetime
from schema_generator import SchemaGenerator, R, O, SchemaAttributes, T
from models.post_model import Post as PostModel
from enums.status import Status

class Post(SchemaAttributes):
    id = T(int)
    title = T(str)
    content = T(str)
    published_at = T(datetime)
    status = T(Status)
    user = T("User")

class PostSchemas:
    generator = SchemaGenerator(PostModel, Post, "Post")

    CREATE = generator.new_schema(
        "Create",
        Post.ALL, R(Post.id)
    )

    PATCH = generator.new_schema(
        "Patch",
        O(CREATE), Post.id
    )

    READ_ALL = generator.new_schema(
        "ReadAll",
        Post.ALL
    )

    READ = generator.new_schema(
        "Read",
        Post.ALL, R(Post.ENTITIES)
    )