from datetime import timedelta

from pydantic import BaseModel, Field
from typing import List
from _utils import (
    export_schema,
    bonsai_sgen,
    BonsaiSgenSerializers,
    pascal_to_snake_case,
)
from pathlib import Path


class Optogenetics(BaseModel):
    use_opto: bool = Field()
    duration: float = Field(ge=0)
    use_pulses: bool = Field()
    ramp_time: float = Field(ge=0)
    frequency: float = Field(gt=0)
    pulse_duration: float = Field(ge=0)


class TimeConstrains(BaseModel):
    min_value: float = Field(ge=0)
    delta: float = Field(ge=0)
    target: float = Field(ge=0)


OptoOnsetTime = TimeConstrains
SoundOnsetTime = TimeConstrains
ReactionTime = TimeConstrains
LnpTime = TimeConstrains


class FixationTime(BaseModel):
    opto_onset_time: OptoOnsetTime = Field()
    sound_onset_time: SoundOnsetTime = Field()


class Sound(BaseModel):
    abl_list: List[float] = Field()
    cycle_ild: bool = Field()


class Session(BaseModel):
    number: int = Field(description="The number of the current session")
    duration: timedelta = Field(description="The duration of the session")
    type: int = Field(description="The number of the session type")
    setup_id: int = Field(description="ID of the setup where the animal will perform the current session")
    starting_trial_number: int = Field(ge=1)
    starting_block_number: int = Field(ge=1)
    starting_training_level: int = Field(ge=1)
    last_training_level: int = Field(ge=1)


class Animal(BaseModel):
    animal_id: int = Field(description="ID of the animal")
    session: Session = Field()
    sound: Sound = Field()
    fixation_time: FixationTime = Field()
    reaction_time: ReactionTime = Field()
    max_reaction_time: float = Field(ge=0)
    min_movement_time: float = Field(ge=0)
    lnp_time: LnpTime = Field()
    base_reward: float = Field(gt=0)
    optogenetics: Optogenetics = Field()
    autobias_correction: bool = Field()


if __name__ == "__main__":
    json_schema = export_schema(Animal)
    schema_name = Animal.__name__
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
