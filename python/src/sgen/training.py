from pathlib import Path
from typing import List

from pydantic import BaseModel, Field

from sgen._utils import (
    BonsaiSgenSerializers,
    bonsai_sgen,
    export_schema,
    pascal_to_snake_case,
)


class TrialRepetition(BaseModel):
    repeat_errors: bool = Field(
        description="Indicates whether the stimulus is repeated after incorrect responses."
    )
    repeat_aborts: bool = Field(
        description="Indicates whether the stimulus is repeated after aborts."
    )
    repeat_fix_time: bool = Field(
        description="Indicates whether the fixation time is repeated after aborts."
    )


class CriticalPerformance(BaseModel):
    value: float = Field(
        description="The minimum correct answer ratio required to advance to the next block (if use_performance is true).",
        ge=0,
        le=1,
    )
    use_performance: bool = Field(
        description="Indicates whether there is a minimum performance requirement to advance to the next block."
    )


class PenaltyTimes(BaseModel):
    incorrect: float = Field(
        description="The penalty time to be applied when the animal answers incorrectly.",
        ge=0,
    )
    abort: float = Field(
        description="The penalty time to be applied when the animal aborts a trial (except if it's a fixation abort).",
        ge=0,
    )
    fixation_abort: float = Field(
        description="The penalty time to be applied in case of a fixation abort.", ge=0
    )


class ReactionTime(BaseModel):
    turn_sound_off: bool = Field(
        description="Indicates whether the sound should stop playing when the animal leaves the central poke."
    )
    use_min_rt: bool = Field(
        description="Indicates whether there is a minimum reaction time (true) or not (false)."
    )
    use_max_rt: bool = Field(
        description="Indicates whether there is a maximum reaction time (true) or not (false)."
    )


class FixationTime(BaseModel):
    opto_exp_mean: float = Field(
        description="The mean value of the random part of the optogenetics onset time (ms), which follows an exponential distribution.",
        ge=0,
    )
    sound_exp_mean: float = Field(
        description="The mean value of the random part of the sound onset time (ms), which follows an exponential distribution.",
        ge=0,
    )


class ITI(BaseModel):
    value: float = Field(description="The intended ITI duration (s).", ge=0)
    can_reset: bool = Field(
        description="Indicates whether the ITI partially resets if the animal tries to poke in the CNP before it ends."
    )


class ILD(BaseModel):
    step_size: float = Field(
        description="The separation between two consecutive |ILD| values.", gt=0
    )
    num_steps: int = Field(
        description="The number of |ILD| values.",
        ge=1,
    )
    use_log: bool = Field(
        description="Indicates whether to use logarithmic steps between consecutive ILD values."
    )
    log_base: float = Field(description="The base of the logarithm.", gt=0)


class ABL(BaseModel):
    abl_list: List[float] = Field(
        description="The list of ABL values to be used in the task (dB SPL)."
    )
    fixed_abl: float = Field(
        description="The ABL value to use when use_fixed_abl from the training.json file is true (dB).",
        ge=0,
    )
    use_fixed_abl: bool = Field(
        description="Indicates whether the fixed_abl should be used in the fully lateralized trials (true) or not (false)."
    )


class Sound(BaseModel):
    abl: ABL = Field(description="Contains the ABL-related parameters.")
    ild: ILD = Field(description="Contains the ILD-related parameters.")
    fully_lateralized_probability: float = Field(
        description="In the fully lateralized variation of the task, the real ILD value corresponds to the input ABL and the real ABL value corresponds to half of it. For example, if the input ABL value is 50 db SPL, one of the speakers will produce a sound of 50 dB SPL and the other one will produce a sound of 0 dB SPL. This parameter indicates the probability of a trial being fully lateralized in a given training level.",
        ge=0,
        le=1,
    )


class Level(BaseModel):
    level_id: int = Field(description="The ID number of the training level.")
    trials_per_block: int = Field(
        description="The number of trials that a block of the current level has.", ge=1
    )
    sound: Sound = Field(description="Contains the sound-related parameters.")
    iti: ITI = Field(
        description="Contains the parameters related to the Inter-trial Interval."
    )
    max_wait: float = Field(
        description="The maximum allowed time to start the trial (s).", ge=0
    )
    fixation_time: FixationTime = Field(
        description="Contains parameters related to the fixation time."
    )
    reaction_time: ReactionTime = Field(
        description="Contains parameters related to the reaction time."
    )
    max_mt: float = Field(description="The maximum allowed movement time (s).")
    penalty_times: PenaltyTimes = Field(
        description="Contains the penalty times for different ocasions."
    )
    critical_performance: CriticalPerformance = Field(
        description="Contains the critical performance for the animal to progress to the next level and whether this feature is used or not."
    )
    max_aborts: int = Field(description="NOT IMPLEMENTED!!", ge=1)
    trial_repetition: TrialRepetition = Field(
        description="Contains the conditions for which a certain trial should be repeated."
    )
    speakers: bool = Field(
        description="Indicates whether the animal is using headphones (true) or box speakers (false). At the moment, this parameter doesn't modify the behavior of the task. Perhaps in the future, it might be possible to input the calibration curves of both the box speakers and the headphones so that this parameter switches to the correct calibration curves."
    )


class Training(BaseModel):
    levels: List[Level] = Field(
        description="The list containing the parameters to be used for each training level."
    )


def generate_training():
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
