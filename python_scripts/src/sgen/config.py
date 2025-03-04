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


class Config(BaseModel):
    behavior_port: Annotated[str, StringConstraints(pattern=r"^COM\d+$")] = Field(
        description="The COM port of the Harp Behavior."
    )
    soundcard_port: Annotated[str, StringConstraints(pattern=r"^COM\d+$")] = Field(
        description="The COM port of the Harp SoundCard."
    )
    left_pump_port: Annotated[str, StringConstraints(pattern=r"^COM\d+$")] = Field(
        description="The COM port of the left Harp SyringePump."
    )
    right_pump_port: Annotated[str, StringConstraints(pattern=r"^COM\d+$")] = Field(
        description="The COM port of the right Harp SyringePump."
    )
    currentdriver_port: Annotated[str, StringConstraints(pattern=r"^COM\d+$")] = Field(
        description="The COM port of the Harp CurrentDriver."
    )
    animal_path: str = Field(
        description="The path to the animal.yml configuration file."
    )
    setup_path: str = Field(
        description="The path to the setup.json configuration file."
    )
    training_path: str = Field(
        description="The path to the training.yml configuration file."
    )
    output_path: str = Field(
        description="The path to the output directory, where the output date will be saved."
    )


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
