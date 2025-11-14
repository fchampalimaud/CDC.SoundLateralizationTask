from pathlib import Path
from typing import Annotated, List, Literal

from pydantic import BaseModel, Field
from pydantic.types import StringConstraints

from sgen._utils import (
    BonsaiSgenSerializers,
    bonsai_sgen,
    export_schema,
    pascal_to_snake_case,
)


class Sound(BaseModel):
    index: int = Field(
        description="The index number where the noise is stored in the Harp SoundCard.",
        ge=2,
        le=31,
    )
    duration: float = Field(description="The duration of the noise (s).")


class SyringePumps(BaseModel):
    use_pumps: bool = Field(
        description="Indicates whether the setup uses valves (false) or Harp SyringePumps (true) for reward delivery."
    )
    left_slope: float = Field(
        description="The slope of the calibration curve of the left Harp SyringePump."
    )
    left_intercept: float = Field(
        description="The intercept of the calibration curve of the left Harp SyringePump."
    )
    right_slope: float = Field(
        description="The slope of the calibration curve of the right Harp SyringePump."
    )
    right_intercept: float = Field(
        description="The intercept of the calibration curve of the right Harp SyringePump."
    )


class Lights(BaseModel):
    box_period: float = Field(
        description="The period of the blinking of the box LED (ms).", ge=0
    )
    poke_period: float = Field(
        description="The period of the blinking of the central poke LED (ms).", ge=0
    )
    iti_light: bool = Field(
        description="Indicates whether the box LED should turn of when the new trial is ready (true) or not (false)."
    )
    poke_light: bool = Field(
        description="Indicates whether the central poke LED should turn of when the new trial is ready (true) or not (false)."
    )
    fixation_light: bool = Field(
        description="Indicates whether the central poke LED should blink during fixation time (true) or not (false)."
    )
    penalty_light: bool = Field(
        description="Indicates whether the box LED should blink during penalty times (true) or not (false)."
    )


class Speakers(BaseModel):
    left_slope: float = Field(
        description="The slope of the calibration curve of the left speaker."
    )
    left_intercept: float = Field(
        description="The intercept of the calibration curve of the left speaker."
    )
    right_slope: float = Field(
        description="The slope of the calibration curve of the right speaker."
    )
    right_intercept: float = Field(
        description="The intercept of the calibration curve of the right speaker."
    )


class Poke(BaseModel):
    low_to_high: bool = Field(
        description="Indicates whether the poke is a low-to-high (true) or a high-to-low (false) device."
    )


class Camera(BaseModel):
    use_camera: bool = Field(
        description="Indicates whether the setup has a camera (true) or not (false)."
    )
    type: Literal["Point Grey", "FLIR"] = Field(
        description="The type of camera used in the setup."
    )
    frames_per_second: float = Field(
        description="The number of frames per second of the camera.", gt=0
    )
    resolution: Annotated[str, StringConstraints(pattern=r"^\d{3,4}x\d{3,4}$")] = Field(
        description="The resolution with which the camera is recording the video."
    )
    codec: Literal["h264", "h264_amf"] = Field(
        description="The codec used to save the video with FFMPEG."
    )


class Setup(BaseModel):
    setup_id: int = Field(description="The ID number of the setup.")
    left_poke: Poke = Field(description="Contains parameters related to the left poke.")
    center_poke: Poke = Field(
        description="Contains parameters related to the center poke."
    )
    right_poke: Poke = Field(
        description="Contains parameters related to the right poke."
    )
    speakers: Speakers = Field(
        description="Contains parameters related to the speakers."
    )
    lights: Lights = Field(
        description="Contains parameters related to the box and poke LEDs."
    )
    syringe_pumps: SyringePumps = Field(
        description="Contains the parameters related to the SyringePumps."
    )
    sounds: List[int] = Field(
        description="The list containing the indexes where the non-short-duration sounds are saved in the Harp SoundCard."
    )
    short_sounds: List[int] = Field(
        description="The list containing the indexes where the short-duration sounds are saved in the Harp SoundCard."
    )
    camera: Camera = Field(description="Contains parameters related to the camera.")


def generate_setup():
    json_schema = export_schema(Setup)
    schema_name = Setup.__name__
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
