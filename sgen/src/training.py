from pydantic import BaseModel, Field
from typing import List
from _utils import (
    export_schema,
    bonsai_sgen,
    BonsaiSgenSerializers,
    pascal_to_snake_case,
)
from pathlib import Path


class Cues(BaseModel):
    iti_light: bool = Field()
    poke_light: bool = Field()
    fixation_light: bool = Field()
    penalty_light: bool = Field()


class TrialRepetition(BaseModel):
    repeat_errors: bool = Field()
    repeat_aborts: bool = Field()


class CriticalPerformance(BaseModel):
    value: float = Field(ge=0, le=1)
    use_performance: bool = Field()


class PenaltyTimes(BaseModel):
    incorrect: float = Field(ge=0)
    abort: float = Field(ge=0)
    fixation_abort: float = Field(ge=0)


class ReactionTime(BaseModel):
    turn_sound_off: bool = Field()
    use_max_rt: bool = Field()


class FixationTime(BaseModel):
    opto_exp_mean: float = Field(ge=0)
    sound_exp_mean: float = Field(ge=0)


class ITI(BaseModel):
    value: float = Field(ge=0)
    can_reset: bool = Field()


class ILD(BaseModel):
    step_size: float = Field(gt=0)
    num_steps: int = Field(ge=1)
    use_log: bool = Field()
    log_base: float = Field(gt=0)


class ABL(BaseModel):
    level_abl: float = Field(ge=0)
    use_level_abl: bool = Field()
    change_every_trial: bool = Field()


class Sound(BaseModel):
    abl: ABL = Field()
    ild: ILD = Field()


class Level(BaseModel):
    level_id: int = Field()
    trials_per_block: int = Field(ge = 1)
    sound: Sound = Field()
    iti: ITI = Field()
    max_wait: float = Field(ge=0)
    fixation_time: FixationTime = Field()
    reaction_time: ReactionTime = Field()
    max_mt: float = Field()
    penalty_times: PenaltyTimes = Field()
    critical_performance: CriticalPerformance = Field()
    max_aborts: int = Field(ge=1)
    trial_repetition: TrialRepetition = Field()
    speakers: bool = Field()
    cues: Cues = Field()


class Training(BaseModel):
    levels: List[Level] = Field()


if __name__ == "__main__":
    json_schema = export_schema(Training)
    schema_name = Training.__name__
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
