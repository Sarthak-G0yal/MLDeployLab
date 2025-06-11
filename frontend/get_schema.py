import requests
from typing import Any, Type
from pydantic import create_model, BaseModel

type_mapping = {
    "string": str,
    "number": float,
    "integer": int,
    "boolean": bool,
    "array": list,
    "object": dict,
}


def get_schema(url: str) -> Type[BaseModel]:
    """Get the schema for the Model model"""
    schema = requests.get(url).json()
    title = schema.get("title", "DynamicModel")
    fields: dict[str, tuple[Any, Any]] = {}
    required = schema.get("required", [])
    properties = schema.get("properties", {})

    for name, meta in properties.items():
        json_type = meta.get("type", "string")
        py_type = type_mapping.get(json_type, Any)
        fields[name] = (py_type, ...) if name in required else (py_type, None)

    # Create dynamic Pydantic model
    dynamic_schema = create_model(schema.get("title", title), **fields)

    return dynamic_schema
