from pydantic import BaseModel, Field
from pydantic.types import StringConstraints
from typing_extensions import Annotated
from typing import Literal
from sgen._utils import (
    export_schema,
    bonsai_sgen,
    BonsaiSgenSerializers,
    pascal_to_snake_case,
)
from pathlib import Path


class Optogenetics(BaseModel):
    opto_trial: bool = Field(
        description="Indicates if optogenetics was used in the current trial."
    )
    duration: float = Field(
        description="The duration of the optogenetics used during the trial (s).", ge=0
    )
    mode: Literal["Left", "Right", "Bilateral"] = Field(description="Indicates the optogenetics mode used in the current session.")


class Outcome(BaseModel):
    response_poke: int = Field(
        description="The answer given by the animal in the current trial.", ge=-1, le=1
    )
    value: int = Field(description="The outcome of the current trial.", ge=-8, le=2)
    block_performance: float = Field(description="The block performance.", ge=0, le=1)
    block_abort_ratio: float = Field(description="The block abort ratio.", ge=0, le=1)


class LnpTime(BaseModel):
    intended_duration: float = Field(
        description="The minimum allowed LNP time (s).", ge=0
    )
    timed_duration: float = Field(description="The timed LNP time (s).", ge=0)


class MovementTime(BaseModel):
    max_duration: float = Field(
        description="The maximum allowed movement time (s).", ge=0
    )
    timed_duration: float = Field(description="The timed movement time (s).", ge=0)


class ReactionTime(BaseModel):
    base_time: float = Field(description="The minimum allowed reaction time (s).", ge=0)
    max_duration: float = Field(
        description="The maximum allowed reaction time (s).", ge=0
    )
    timed_duration: float = Field(description="The timed reaction time (s).", ge=0)


class FixationTimeParts(BaseModel):
    base_time: float = Field(
        description="The constant part of the fixation time (ms).", ge=0
    )
    exp_mean: float = Field(
        description="The mean value of the random part of the fixation time (ms), which follows an exponential distribution.",
        ge=0,
    )
    intended_duration: float = Field(
        description="The intended duration for this part of the fixation time (ms).",
        ge=0,
    )
    timed_duration: float = Field(
        description="The timed duration for this part of the fixation time (ms).", ge=0
    )


OptoOnsetTime = FixationTimeParts
SoundOnsetTime = FixationTimeParts


class FixationTime(BaseModel):
    opto_onset_time: OptoOnsetTime = Field(
        description="Contains the data related to the Optogenetics Onset Time part of the Fixation Time."
    )
    sound_onset_time: SoundOnsetTime = Field(
        description="Contains the data related to the Sound Onset Time part of the Fixation Time."
    )
    intended_duration: float = Field(
        description="The intended duration for the total fixation time (ms).",
        ge=0,
    )
    timed_duration: float = Field(
        description="The timed duration for the total fixation time (ms).", ge=0
    )


class TimeToCnp(BaseModel):
    timed_value: float = Field(
        description="The time it took for the animal to start the trial (s).", ge=0
    )
    max_duration: float = Field(
        description="The maximum allowed time to start the trial (s).", ge=0
    )


class ITI(BaseModel):
    intended_duration: float = Field(
        description="The intended duration of the ITI (s).", ge=0
    )
    start_time: float = Field(
        description="The timestamp at which the trial started (s).", ge=0
    )
    end_time: float = Field(
        description="The timestamp at which the trial ended (s).", ge=0
    )
    timed_duration: float = Field(description="The ITI duration (s).", gt=0)


class Sound(BaseModel):
    abl: float = Field(description="The trial ABL value (dB).", ge=0)
    ild: float = Field(description="The trial ILD value (dB).")
    sound_index: int = Field(
        description="The index of the sound that played in the trial.", ge=2, le=31
    )
    left_amplification: float = Field(
        description="The amplification applied to the left speaker in the trial."
    )
    right_amplification: float = Field(
        description="The amplification applied to the right speaker in the trial."
    )


class Session(BaseModel):
    number: int = Field(description="The number of the current session.")
    type: int = Field(description="The number of the session type.")
    setup_id: int = Field(
        description="The ID number of the setup where the animal will performed the trial."
    )


class Block(BaseModel):
    number: int = Field(description="The block number.")
    training_level: int = Field(description="The training level of the current block.")
    trials_per_block: int = Field(
        description="The number of trials that the current block is expected to have.",
        ge=1,
    )


class Trial(BaseModel):
    number: int = Field(description="The trial number.", ge=1)
    start_time: float = Field(
        description="The timestamp at which the trial started (s).", ge=0
    )
    tared_start_time: float = Field(description="The tared timestamp at which the trial started in which t = 0 is the start time of the first trial of the session (s).", ge=0)
    end_time: float = Field(
        description="The timestamp at which the trial ended (s).", ge=0
    )
    duration: float = Field(description="The trial duration (s).", gt=0)


class Output(BaseModel):
    animal_id: int = Field(description="The ID number of the animal.")
    version: Annotated[str, StringConstraints(pattern=r'\d+\.\d+\.\d+')] = Field(description="The version of the project used in the session.")
    trial: Trial = Field(description="Contains the trial-related data.")
    block: Block = Field(description="Contains the block-related data.")
    session: Session = Field(description="Contains the session-related data.")
    sound: Sound = Field(description="Contains the sound-related data.")
    iti: ITI = Field(description="Contains the ITI-related data.")
    time_to_cnp: TimeToCnp = Field(
        description="Contains the data related to the time to CNP."
    )
    fixation_time: FixationTime = Field(
        description="Contains the data related to the fixation time."
    )
    reaction_time: ReactionTime = Field(
        description="Contains the data related to the reaction time."
    )
    movement_time: MovementTime = Field(
        description="Contains the data related to the movement time."
    )
    lnp_time: LnpTime = Field(description="Contains the data related to the LNP time.")
    outcome: Outcome = Field(
        description="Contains the data related to the trial outcome."
    )
    repeated_trial: bool = Field(
        description="Indicates whether the current trial is a repetition of the previous trial (true) or not (false)."
    )
    optogenetics: Optogenetics = Field(
        description="Contains the data related to optogenetics."
    )


def generate_output():
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
