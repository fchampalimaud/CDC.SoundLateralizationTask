from pathlib import Path
from typing import Dict

from pydantic import BaseModel, Field

from sgen._utils import (
    BonsaiSgenSerializers,
    bonsai_sgen,
    export_schema,
    pascal_to_snake_case,
)


class Print(BaseModel):
    text: str = Field(description="The text to be printed.")
    units: str = Field(
        description="The units of the quantity being printed (if necessary)."
    )


class PrintDict(BaseModel):
    prints: Dict[str, Print] = Field(
        description="The dictionary containing all of the task's prints."
    )


def generate_prints():
    json_schema = export_schema(PrintDict)
    schema_name = PrintDict.__name__
    _dashed = pascal_to_snake_case(schema_name).replace("_", "-")
    schema_path = Path(rf"../src/config/schemas/{_dashed}-schema.json")
    with open(schema_path, "w", encoding="utf-8") as f:
        f.write(json_schema)

    bonsai_sgen(
        schema_path=schema_path,
        output_path=Path(rf"../src/Extensions"),
        namespace=schema_name,
        serializer=[BonsaiSgenSerializers.JSON, BonsaiSgenSerializers.YAML],
    )
