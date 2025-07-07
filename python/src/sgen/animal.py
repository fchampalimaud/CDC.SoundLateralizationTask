from datetime import timedelta
from pathlib import Path
from typing import List, Literal

from pydantic import BaseModel, Field
from pydantic.types import StringConstraints
from typing_extensions import Annotated

from sgen._utils import (
    BonsaiSgenSerializers,
    bonsai_sgen,
    export_schema,
    pascal_to_snake_case,
)


class AutobiasCorrection(BaseModel):
    use_correction: bool = Field(
        description="Indicates whether the autobias correction feature should be used or not."
    )
    window: int = Field(
        description="The amount of trials to consider to calculate the animal bias.",
        gt=0,
    )
    cutoff_bias: float = Field(
        description="The minimum |bias| value from which the side rewards start to be corrected.",
        ge=0,
        le=1,
    )
    performance_threshold: float = Field(
        description="The minimum performance value for which the side rewards are not corrected.",
        ge=0,
        le=1,
    )
    slope_multiplier: float = Field(
        description="A multiplying factor to the slope of the increasing reward amount side (corresponds to the non-biased side).",
        gt=0,
    )


class OptoLED(BaseModel):
    voltage: float = Field(
        description="The voltage to use in the TTL signal.", ge=0, le=5000
    )
    power: float = Field(
        description="The power with which the animal is stimulated.", ge=0
    )
    mode: Literal["TTL", "Current"] = Field(
        description="Indicates whether the LED port is being used to control an external LED via TTL or if it's controlling a LED directly with the current sources."
    )
    use_pulses: bool = Field(
        description="Indicates whether the optogenetics protocol uses pulses of light (true) or a continuous emission (false)."
    )
    frequency: int = Field(
        description="The frequency of the pulses (Hz). It only works when use_pulses is true.",
        ge=1,
        le=255,
    )
    duty_cycle: int = Field(
        description="The duty cycle of the pulses (%). It only works when use_pulses is true.",
        ge=0,
        le=100,
    )


class Optogenetics(BaseModel):
    use_opto: bool = Field(description="Indicates whether optogenetics is used or not.")
    mode: Literal["Left", "Right", "Bilateral"] = Field(
        description="Indicates the optogenetics mode used in the current session."
    )
    duration: float = Field(
        description="The duration of the optogenetics stimulation/inhibition protocol (s).",
        ge=0,
    )
    opto_ratio: float = Field(
        description="The ratio of optogenetics trials.", ge=0, le=1
    )
    use_rt: bool = Field(
        description="Indicates whether the optogenetics stimulation/inhibition should stop when the animal leaves the poke (true) or not (false)."
    )
    ramp_mode: Literal["None", "Rise", "Fall", "Both"] = Field(
        description="Indicates the ramp mode used in the optogenetics protocol. It only works if the LED is not configured to use pulses."
    )
    ramp_time: int = Field(
        description="The duration of the ramp of the optogenetics protocol (ms). It only works when use_pulses is false.",
        ge=1,
    )
    led0: OptoLED = Field(description="The optogenetics protocol that LED 0 executes.")
    led1: OptoLED = Field(description="The optogenetics protocol that LED 1 executes.")


class TimeConstrains(BaseModel):
    min_value: float = Field(description="The initial base value.", ge=0)
    delta: float = Field(
        description="The increment to the base value every trial a certain condition is met until the target value is reached.",
        ge=0,
    )
    target: float = Field(description="The target value.", ge=0)


OptoOnsetTime = TimeConstrains
SoundOnsetTime = TimeConstrains
ReactionTime = TimeConstrains
LnpTime = TimeConstrains


class FixationTime(BaseModel):
    opto_onset_time: OptoOnsetTime = Field(
        description="Contains parameters related to the Optogenetics Onset Time part of the Fixation Time. The units of each of the parameters is milliseconds."
    )
    sound_onset_time: SoundOnsetTime = Field(
        description="Contains parameters related to the Sound Onset Time part of the Fixation Time. The units of each of the parameters is milliseconds."
    )


class Sound(BaseModel):
    fixed_abl: float = Field(
        description="The ABL value to use when use_fixed_abl from the training.json file is true (dB).",
        ge=0,
    )
    abl_list: List[float] = Field(
        description="The list of ABL values to be used in the task (dB SPL)."
    )
    pseudo_random_side: bool = Field(
        description="Indicates whether the correct side is picked pseudo-randomly (true) or randomly (false). If it's picked pseudo-randomly, a shuffled array with equal amounts of -1's (left) and 1's (right) of size 2 * `max_side` is created and it's cycled through - a new shuffled array is generated when the end of the array is reached."
    )
    max_side: int = Field(
        description="The maximum amount of elements representing the left or right side in the pseudo-random array for when the side is picked pseudo-randomly.",
        gt=0,
    )


class Session(BaseModel):
    number: int = Field(description="The number of the current session.", gt=0)
    experimenter: str = Field(
        description="The person who trained the animal in the current session."
    )
    duration: timedelta = Field(
        description="The duration of the session (in the hh:mm:ss format)."
    )
    type: int = Field(description="The number of the session type.")
    starting_trial_number: int = Field(
        description="The number of the first trial of the session.", ge=1
    )
    block_number: int = Field(
        description="The number of the first block of the session.", ge=1
    )
    starting_training_level: int = Field(
        description="The training level the animal will start in the current session.",
        ge=1,
    )
    last_training_level: int = Field(
        description="The last training level the animal is allowed to progress to in the current session.",
        ge=1,
    )


class Animal(BaseModel):
    animal_id: Annotated[str, StringConstraints(pattern=r"^[A-Z]{2,6}\d{4}$")] = Field(
        description="The ID of the animal."
    )
    batch: Annotated[str, StringConstraints(pattern=r"^[a-zA-Z0-9_\-\.]+$")] = Field(
        description="The batch to which the current animal belongs to."
    )
    session: Session = Field(description="Contains the session-related parameters.")
    sound: Sound = Field(description="Contains the sound-related parameters.")
    fixation_time: FixationTime = Field(
        description="Contains parameters related to the fixation time."
    )
    reaction_time: ReactionTime = Field(
        description="Contains parameters related to the reaction time. The units of each of the parameters is seconds."
    )
    max_reaction_time: float = Field(
        description="The maximum allowed reaction time (s).", ge=0
    )
    min_movement_time: float = Field(
        description="The minimum allowed movement time (s).", ge=0
    )
    lnp_time: LnpTime = Field(
        description="Contains parameters related to the LNP (Lateral Nose Poke) time. The units of each of the parameters is seconds."
    )
    base_reward: float = Field(
        description="The amount of reward delivered to the animal (uL).", gt=0
    )
    optogenetics: Optogenetics = Field(
        description="Contains the optogenetics-related parameters."
    )
    autobias_correction: AutobiasCorrection = Field(
        description="Contains parameters related to the autobias correction algorithm."
    )


def generate_animal():
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
