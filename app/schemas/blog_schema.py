from pydantic import BaseModel, Field
from datetime import datetime
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler): 
        from pydantic_core import core_schema

        return core_schema.union_schema(
            [
                core_schema.is_instance_schema(ObjectId),
                core_schema.chain_schema(
                    [
                        core_schema.str_schema(),
                        core_schema.no_info_plain_validator_function(cls.validate), 
                    ]
                ),
            ],
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda x: str(x)
            ),
        )

    @classmethod
    def validate(cls, v): 
        if isinstance(v, ObjectId):
            return v
        if isinstance(v, str):
            if ObjectId.is_valid(v):
                return ObjectId(v)
        raise ValueError("Invalid ObjectId")


class PostCreateSchema(BaseModel):
    """ Schema for creating a blog post. """
    title: str = Field(..., min_length=3, max_length=50)
    content: str = Field(..., min_length=10, max_length=500)
    category: str = Field(..., min_length=3, max_length=20)
    tags: list[str] = Field(default_factory=list)
    
class PostResponseSchema(PostCreateSchema):
    """ Schema for the response of a blog post. """
    id: PyObjectId = Field(default_factory=PyObjectId, alias="id")
    created_at: datetime
    updated_at: datetime
    
    model_config = {
        "from_attributes": True
    }