from typing import List
from schema_generator import SchemaGenerator, R, O, SchemaAttributes, T
from models.user_model import User as UserModel
from schema_generator.verifiers import one_of

class User(SchemaAttributes):
    id = T(int)
    email = T(str)
    firstname = T(str)
    lastname = T(str)
    location_id = T(int)
    posts = T(List["Post"]) # Specifying a string will allow a different schema to be used depending on the schema the attribute is in.
                            # For example, in the UserPatch schema, the PostPatch schema will be used (and therefore in this case the attribute 'posts' will be equal to List[PostPatch])
    location = T("Location")

class UserSchemas:
    generator = SchemaGenerator(UserModel, User, "User")

    CREATE = generator.new_schema(
        "Create",
        User.ALL, O(User.location, User.location_id), R(User.id), # .ALL retrieve all the attributes and the R(User.ENTITIES) allows to delete the attributes which are linked to other schemas
        verifiers={"*": [one_of(User.location, User.location_id)]} # Verifiers are used to validate attributes (it can also be '*' if you don't need a specific attribute)
    )

    PATCH = generator.new_schema(
        "Patch",
        O(CREATE), User.id # O makes attributes optional
    )

    READ_ALL = generator.new_schema(
        "ReadAll",
        User.ALL # .ALL retrieves all attributes
    )

    READ = generator.new_schema(
        "Read",
        User.ALL, R(User.ENTITIES) # R allows to remove attributes from the schema
    )