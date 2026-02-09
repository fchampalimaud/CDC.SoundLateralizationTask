# Optogenetics

An experimental setup that uses this project for behavioral experiments and is equipped with a [Harp CurrentDriver](https://github.com/fchampalimaud/device.currentdriver) and a laser/LED that can be externally controlled is able to run an optogenetics session.

In the context of the this task, an optogenetics stimulation starts during the fixation time, at the opto onset time to be more precise (a description of the fixation time can be found [here](state-machine.md#fixation-time)). The stimulation ends either when the animal leaves the central port (if `optogenetics.use_rt` is `true`) or after a fixed amount of time (that starts when the stimulus is presented).

## How to configure an optogenetics session?
For a session to use the optogenetics feature the `optogenetics.use_opto` parameter of the `animal.yml` file must be set to `true`. See below an example for a configuration of an optogenetics session.

```
optogenetics:
  use_opto: true
  mode: Left Excitation
  duration: 2
  opto_ratio: 0.3
  use_rt: false
  ramp_mode: Fall
  ramp_time: 100
  led0:
    voltage: 2000
    power: 10
    mode: TTL
    use_pulses: false
    frequency: 20
    duty_cycle: 50
  led1:
    voltage: 0
    power: 0
    mode: TTL
    use_pulses: false
    frequency: 1
    duty_cycle: 50
```

From the snippet above, it can be concluded that it's possible to configure a variety of optogenetics protocol. Here is a list of what can be configured:
- The ratio of optogenetics trials in a session (`opto_ratio`).
- The use of rise and/or fall ramps of variable duration (`ramp_time`) when using a continuous stimulation protocol (i.e. `ledx.use_pulses` is `false`). The `ramp_mode` parameter can take the values `None`, `Rise`, `Fall` and `Both`.
- Up to 2 different LEDs/lasers:
  - The voltage with which the LED will be controlled.
  - Whether the LED is being controlled externally or directly (current driven).
  - The possibility of using a pulsed protocol (if `use_pulses` is true). To define the characteristics of the pulses, the `frequency` and `duty_cycle` parameters can be modified.

Some of the parameters that can be defined (such as `mode` and `led0.power`) don't modify the protocol, but can be used as a record:
- The `mode` parameter can take one of the following values: `None`, `Left Excitation`, `Right Excitation`, `Bilateral Excitation`, `Left Inhibition`, `Right Inhibition`, `Bilateral Inhibition`, `Left Excitation Right Inhibition` and `Left Inhibition Right Excitation`.

An example of an `animal.yml` file with an optogenetics session configured is shown below.

```
# yaml-language-server: $schema=../src/config/schemas/animal-schema.json
animal_id: ANIMAL0000
batch: batch_name
session:
  number: 1
  duration: 02:00:00
  experimenter: experimenter_name
  type: 1
  starting_trial_number: 1
  starting_training_level: 1
  last_training_level: 3
  block_number: 1
sound:
  pseudo_random_side: false
  max_side: 8
fixation_time:
  opto_onset_time:
    min_value: 5
    delta: 0.5
    target: 100
  sound_onset_time:
    min_value: 5
    delta: 0.5
    target: 100
reward:
  base_amount: 15
optogenetics:
  use_opto: true
  mode: Left Excitation
  duration: 2
  opto_ratio: 0.3
  use_rt: false
  ramp_mode: Fall
  ramp_time: 100
  led0:
    voltage: 2000
    power: 10
    mode: TTL
    use_pulses: false
    frequency: 20
    duty_cycle: 50
  led1:
    voltage: 0
    power: 0
    mode: TTL
    use_pulses: false
    frequency: 1
    duty_cycle: 50
```