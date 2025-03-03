from sgen.animal import generate_animal
from sgen.output import generate_output
from sgen.prints import generate_prints
from sgen.setup import generate_setup
from sgen.training import generate_training
from sgen.config import generate_config


def main():
    generate_animal()
    generate_output()
    generate_prints()
    generate_setup()
    generate_training()
    generate_config()
