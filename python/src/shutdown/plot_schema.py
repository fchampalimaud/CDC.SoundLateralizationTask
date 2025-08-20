from pathlib import Path
from typing import List, Literal

from pydantic import BaseModel, Field
from sgen._utils import (
    export_schema,
    pascal_to_snake_case,
)


class Line(BaseModel):
    condition: str = Field(
        description="The condition that filters the data to be plotted."
    )
    marker: Literal["<", ">", "o", "o-"] = Field(description="The marker to be used.")
    color: str = Field(description="The color to be used.")


class Plot(BaseModel):
    name: str = Field(description="The name of the plot.")
    x: int = Field(description="The x coordinate of the plot.", ge=0, le=2)
    y: int = Field(description="The y coordinate of the plot.", ge=0, le=2)
    xlabel: str = Field(description="The label of the x-axis of the plot.")
    ylabel: str = Field(description="The label of the y-axis of the plot.")
    lines: List[Line] = Field(
        description="Contains the parameters for each line in the plot."
    )


def generate_plot():
    json_schema = export_schema(Plot)
    schema_name = Plot.__name__
    _dashed = pascal_to_snake_case(schema_name).replace("_", "-")
    schema_path = Path(rf"../src/config/schemas/{_dashed}-schema.json")
    with open(schema_path, "w", encoding="utf-8") as f:
        f.write(json_schema)


generate_plot()
