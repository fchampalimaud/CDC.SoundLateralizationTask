from pydantic import BaseModel, Field
from pydantic.types import StringConstraints
from typing_extensions import Annotated
from sgen._utils import (
    export_schema,
    bonsai_sgen,
    BonsaiSgenSerializers,
    pascal_to_snake_case,
)
from pathlib import Path


class Ports(BaseModel):
    behavior: Annotated[str, StringConstraints(pattern=r"^COM\d+$")] = Field(
        description="The COM port of the Harp Behavior."
    )
    soundcard: Annotated[str, StringConstraints(pattern=r"^COM\d+$")] = Field(
        description="The COM port of the Harp SoundCard."
    )
    left_pump: Annotated[str, StringConstraints(pattern=r"^COM\d+$")] = Field(
        description="The COM port of the left Harp SyringePump."
    )
    right_pump: Annotated[str, StringConstraints(pattern=r"^COM\d+$")] = Field(
        description="The COM port of the right Harp SyringePump."
    )
    currentdriver: Annotated[str, StringConstraints(pattern=r"^COM\d+$")] = Field(
        description="The COM port of the Harp CurrentDriver."
    )


class Paths(BaseModel):
    animal: Annotated[str, StringConstraints(pattern=r"\.yml$")] = Field(
        description="The path to the animal.yml configuration file."
    )
    setup: Annotated[str, StringConstraints(pattern=r"\.csv$")] = Field(
        description="The path to the setup.json configuration file."
    )
    training: Annotated[str, StringConstraints(pattern=r"\.csv$")] = Field(
        description="The path to the training.yml configuration file."
    )
    output: str = Field(
        description="The path to the output directory, where the output date will be saved."
    )


class Config(BaseModel):
    ports: Ports = Field(description="Contains the COM ports for the different Harp boards.")
    paths: Paths = Field(description="Contains the paths to the configuration files and to the output directory.")


def generate_config():
    json_schema = export_schema(Config)
    schema_name = Config.__name__
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
