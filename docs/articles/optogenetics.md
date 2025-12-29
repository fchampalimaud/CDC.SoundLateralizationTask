# Optogenetics

## How to configure an optogenetics session?

```
optogenetics:
  use_opto: true
  mode: Bilateral
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
  mode: Bilateral
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