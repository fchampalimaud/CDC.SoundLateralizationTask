from pydantic import BaseModel, Field
from typing import List
from _utils import (
    export_schema,
    bonsai_sgen,
    BonsaiSgenSerializers,
    pascal_to_snake_case,
)
from pathlib import Path


class Sound(BaseModel):
    index: int = Field(ge=2, le=31)
    duration: float = Field()


class SyringePumps(BaseModel):
    use_pumps: bool = Field()
    left_slope: float = Field()
    left_intercept: float = Field()
    right_slope: float = Field()
    right_intercept: float = Field()


class Lights(BaseModel):
    box_period: float = Field(ge=0)
    box_duty_cycle: float = Field(ge=0, le=1)
    poke_period: float = Field(ge=0)
    poke_duty_cycle: float = Field(ge=0, le=1)


class Speakers(BaseModel):
    left_slope: float = Field()
    left_intercept: float = Field()
    right_slope: float = Field()
    right_intercept: float = Field()


class Poke(BaseModel):
    low_to_high: bool = Field()


class Setup(BaseModel):
    setup_id: int = Field()
    left_poke: Poke = Field()
    center_poke: Poke = Field()
    right_poke: Poke = Field()
    speakers: Speakers = Field()
    lights: Lights = Field()
    syringe_pumps: SyringePumps = Field()
    sounds: List[Sound] = Field()


class SetupList(BaseModel):
    setups: List[Setup] = Field()


if __name__ == "__main__":
    json_schema = export_schema(SetupList)
    schema_name = SetupList.__name__
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

    # experiment_example = Animal(
    #     animal_id="my_mouse",
    #     trials=[
    #         Trial(inter_trial_interval=1.0, reward_amount=1),
    #         Trial(inter_trial_interval=0.5, reward_amount=0),
    #     ],
    # )

    # with open(
    #     rf"src/json/{_dashed}-example.json",
    #     "w",
    #     encoding="utf-8",
    # ) as f:
    #     f.write(experiment_example.model_dump_json(indent=2)) 
