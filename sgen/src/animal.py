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
    use_opto: bool = Field(description="Indicates whether optogenetics is used or not.")
    duration: float = Field(description="The duration of the optogenetics stimulation/inhibition protocol (s).", ge=0)
    use_pulses: bool = Field(description="Indicates whether the optogenetics protocol uses pulses of light (true) or a continuous emission (false).")
    ramp_time: float = Field(description="The duration of the ramp of the optogenetics protocol (ms). It only works when use_pulses is false.", ge=0)
    frequency: float = Field(description="The frequency of the pulses (Hz). It only works when use_pulses is true.", gt=0)
    pulse_duration: float = Field(description="The duration of a single pulse (ms). It only works when use_pulses is true.", ge=0)


class TimeConstrains(BaseModel):
    min_value: float = Field(description="The initial base value.", ge=0)
    delta: float = Field(description="The increment to the base value every trial a certain condition is met until the target value is reached.", ge=0)
    target: float = Field(description="The target value.", ge=0)


OptoOnsetTime = TimeConstrains
SoundOnsetTime = TimeConstrains
ReactionTime = TimeConstrains
LnpTime = TimeConstrains


class FixationTime(BaseModel):
    opto_onset_time: OptoOnsetTime = Field(description="Contains parameters related to the Optogenetics Onset Time part of the Fixation Time. The units of each of the parameters is milliseconds.")
    sound_onset_time: SoundOnsetTime = Field(description="Contains parameters related to the Sound Onset Time part of the Fixation Time. The units of each of the parameters is milliseconds.")


class Sound(BaseModel):
    fixed_abl: float = Field(description="The ABL value to use when use_fixed_abl from the training.json file is true (dB).", ge=0)
    abl_list: List[float] = Field(description="The list of ABL values to be used in the task (dB SPL).")
    cycle_ild: bool = Field(description="If true, the ILD array is shuffled and the ILD is picked by just following the new array order; when the end of the array is reached, the array is shuffled again and the procedure is repeated. Otherwise, an ILD value is randomly picked every trial from the array of ILDs.")


class Session(BaseModel):
    number: int = Field(description="The number of the current session.")
    duration: timedelta = Field(description="The duration of the session (in the hh:mm:ss format).")
    type: int = Field(description="The number of the session type.")
    setup_id: int = Field(description="The ID number of the setup where the animal will perform the session.")
    starting_trial_number: int = Field(description="The number of the first trial of the session.", ge=1)
    starting_block_number: int = Field(description="The number of the first block of the session.", ge=1)
    starting_training_level: int = Field(description="The training level the animal will start in the current session.", ge=1)
    last_training_level: int = Field(description="The last training level the animal is allowed to progress to in the current session.", ge=1)


class Animal(BaseModel):
    animal_id: int = Field(description="The ID number of the animal.")
    session: Session = Field(description="Contains the session-related parameters.")
    sound: Sound = Field(description="Contains the sound-related parameters.")
    fixation_time: FixationTime = Field(description="Contains parameters related to the fixation time.")
    reaction_time: ReactionTime = Field(description="Contains parameters related to the reaction time. The units of each of the parameters is seconds.")
    max_reaction_time: float = Field(description="The maximum allowed reaction time (s).", ge=0)
    min_movement_time: float = Field(description="The minimum allowed movement time (s).", ge=0)
    lnp_time: LnpTime = Field(description="Contains parameters related to the LNP (Lateral Nose Poke) time. The units of each of the parameters is seconds.")
    base_reward: float = Field(description="The amount of reward delivered to the animal (uL).", gt=0)
    optogenetics: Optogenetics = Field(description="Contains the optogenetics-related parameters.")
    autobias_correction: bool = Field(description="Indicates whether autobias correction should be applied or not.")


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