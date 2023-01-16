from datetime import datetime
from schema_generator import SchemaGenerator, R, O, SchemaAttributes, T
from models.location_model import Location as LocationModel
from enums.status import Status

class Location(SchemaAttributes):
    id = T(int)
    address = T(str)
    postal_code = T(str)
    country_code = T(str)

class LocationSchemas:
    generator = SchemaGenerator(LocationModel, Location, "Location")

    CREATE = generator.new_schema(
        "Create",
        Location.ALL, R(Location.id)
    )

    PATCH = generator.new_schema(
        "Patch",
        O(CREATE), Location.id
    )

    READ = generator.new_schema(
        "Read",
        Location.ALL, R(Location.ENTITIES)
    )