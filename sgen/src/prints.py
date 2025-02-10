from pydantic import BaseModel, Field
from typing import Dict
from _utils import (
    export_schema,
    bonsai_sgen,
    BonsaiSgenSerializers,
    pascal_to_snake_case,
)
from pathlib import Path


class Print(BaseModel):
    text: str = Field(description="The text to be printed.")
    units: str = Field(description="The units of the quantity being printed (if necessary).")


class PrintDict(BaseModel):
    prints: Dict[str, Print] = Field(description="The dictionary containing all of the task's prints.")


if __name__ == "__main__":
    json_schema = export_schema(PrintDict)
    schema_name = PrintDict.__name__
    _dashed = pascal_to_snake_case(schema_name).replace("_", "-")
    schema_path = Path(rf"../src/config/schemas/{_dashed}-schema.json")
    with open(schema_path, "w", encoding="utf-8") as f:
        f.write(json_schema)

    bonsai_sgen(
        schema_path=schema_path,
        output_path=Path(rf"../src/Extensions/{schema_name}.cs"),
        namespace=schema_name,
        serializer=[BonsaiSgenSerializers.JSON, BonsaiSgenSerializers.YAML],
    )
