from pydantic import BaseModel, Field
from _utils import (
    export_schema,
    bonsai_sgen,
    BonsaiSgenSerializers,
    pascal_to_snake_case,
)
from pathlib import Path


class Optogenetics(BaseModel):
    opto_trial: bool = Field()
    duration: float = Field(ge=0)
    left_power: float = Field(ge=0)
    right_power: float = Field(ge=0)


class Outcome(BaseModel):
    response_poke: int = Field(ge=-1, le=1)
    value: int = Field(ge=-8, le=2)
    block_performance: float = Field(ge=0, le=1)
    block_abort_ratio: float = Field(ge=0, le=1)


class LnpTime(BaseModel):
    intended_duration: float = Field(ge=0)
    timed_duration: float = Field(ge=0)


class MovementTime(BaseModel):
    max_duration: float = Field(ge=0)
    timed_duration: float = Field(ge=0)


class ReactionTime(BaseModel):
    base_time: float = Field(ge=0)
    max_duration: float = Field(ge=0)
    timed_duration: float = Field(ge=0)


class FixationTimeParts(BaseModel):
    base_time: float = Field(ge=0)
    exp_mean: float = Field(ge=0)
    intended_duration: float = Field(ge=0)
    timed_duration: float = Field(ge=0)


OptoOnsetTime = FixationTimeParts
SoundOnsetTime = FixationTimeParts


class FixationTime(BaseModel):
    opto_onset_time: OptoOnsetTime = Field()
    sound_onset_time: SoundOnsetTime = Field()


class TimeToCnp(BaseModel):
    timed_value: float = Field(ge=0)
    max_duration: float = Field(ge=0)


class ITI(BaseModel):
    intended_duration: float = Field(ge=0)
    start_time: float = Field(ge=0)
    end_time: float = Field(ge=0)
    timed_duration: float = Field(gt=0)


class Sound(BaseModel):
    abl: float = Field(ge=0)
    ild: float = Field()
    sound_index: int = Field(ge=2, le=31)
    left_amplification: float = Field()
    right_amplification: float = Field()


class Session(BaseModel):
    number: int = Field(description="The number of the current session")
    type: int = Field(description="The number of the session type")
    setup_id: int = Field(description="ID of the setup where the animal will perform the current session")


class Block(BaseModel):
    number: int = Field()
    training_level: int = Field()
    trials_per_block: int = Field(ge=1)


class Trial(BaseModel):
    number: int = Field(ge=1)
    start_time: float = Field(ge=0)
    end_time: float = Field(ge=0)
    duration: float = Field(gt=0)


class Output(BaseModel):
    animal_id: int = Field(description="ID of the animal")
    trial: Trial = Field()
    block: Block = Field()
    session: Session = Field()
    sound: Sound = Field()
    iti: ITI = Field()
    time_to_cnp: TimeToCnp = Field()
    fixation_time: FixationTime = Field()
    reaction_time: ReactionTime = Field()
    movement_time: MovementTime = Field()
    lnp_time: LnpTime = Field()
    outcome: Outcome = Field()
    repeated_trial: bool = Field()
    optogenetics: Optogenetics = Field()


if __name__ == "__main__":
    json_schema = export_schema(Output)
    schema_name = Output.__name__
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
