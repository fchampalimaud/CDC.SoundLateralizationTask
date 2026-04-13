# Optogenetics

An experimental setup that uses this project for behavioral experiments and is equipped with a [Harp CurrentDriver](https://github.com/fchampalimaud/device.currentdriver) and a laser/LED that can be externally controlled is able to run an optogenetics session.

In the context of this task, an optogenetics stimulation starts either during the fixation time (see how to define the conditions for this case [here](fixation-time.md#example-optogenetics)) or at stimulus onset. The stimulation ends either when the animal leaves the central port (if `optogenetics.use_rt` is `true`) or after a fixed duration.

## How to configure an optogenetics session?
For a session to use the optogenetics feature the `optogenetics.use_opto` parameter of the `animal.yml` file must be set to `true`. 

After that, and after setting the ratio of optogenetics trials in the session (`opto_ratio` parameter), the user must define the number of protocols it desires to be used throughout the session under the `protocols` parameter. Each protocol is defined by:
- Duration (ms)
- Probability of this protocol being picked given that the current trial will be an optogenetics one (the final probability is normalized relative to sum of the `probability` parameters of every defined protocol)
- The onset moment (`MidFixation` or `SoundStart`)
- Protocol delay, i.e. the amount of time after the onset moment at which the protocol should actually start (ms)
- Whether the optogenetics stimulation should end when the animal leaves the CNP (`use_rt` parameter)
- Ramp (only available for continuous optogenetics stimulation)
  - Mode (`None`, `Rise`, `Fall`, `Both`)
  - Duration (ms)
- The characteristics for each light source (`led0` and `led1` parameters)
  - Voltage (mV)
  - Whether to use pulses or continuous stimulation (`use_pulses` parameter)
  - Pulse frequency (`frequency`)
  - Pulse duty cycle (`duty_cycle`)

### Example
In order to understand how to configure a session in practice, let's assume we want to run a session with 2 different optogenetics protocols: a mid-fixation continuous stimulation (75% of optogenetics trials) and a pulsed stimulation that starts 50 ms after the stimulus onset (25% of optogenetics trials). This session can be configured as follows:

```
optogenetics:
  use_opto: true
  opto_ratio: 0.3
  mode: LeftExcitation
  protocols:
    - duration: 0.2
      probability: 3
      onset: MidFixation
      use_rt: false
      ramp_mode: Fall
      ramp_time: 100
      led0:
        voltage: 1000
    - duration: 0.2
      probability: 1
      onset: SoundStart
      protocol_delay: 50
      use_rt: false
      ramp_mode: None
      ramp_time: 1
      led0:
        voltage: 1000
        use_pulses: true
        frequency: 20
        duty_cycle: 50
```

Note that it's possible to define a parameter called `optogenetics.mode`. This parameter is purely informative for the user to know what kind of stimulation was made in the current session. This parameter can take one of the following values: `None`, `LeftExcitation`, `RightExcitation`, `BilateralExcitation`, `LeftInhibition`, `RightInhibition`, `BilateralInhibition`, `LeftExcitationRightInhibition` or `LeftInhibitionRightExcitation`.

To know how the snippet above can be incorporated in an `animal.yml` file, see the example below:

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
  training:
    min_value: 10
    delta: 1
    target: 200
  task:
    - distribution: constant
      value: 100
      opto_onset: true
    - distribution: exponential
      mean: 200
      max_value: 1000
      opto_onset: true
    - distribution: constant
      value: 100
    - distribution: exponential
      mean: 200
      max_value: 1000
reward:
  base_amount: 15
optogenetics:
  use_opto: true
  opto_ratio: 0.3
  mode: LeftExcitation
  protocols:
    - duration: 0.2
      probability: 1
      onset: MidFixation
      use_rt: false
      ramp_mode: Fall
      ramp_time: 100
      led0:
        voltage: 1000
    - duration: 0.2
      probability: 1
      onset: SoundStart
      protocol_delay: 50
      use_rt: false
      ramp_mode: None
      ramp_time: 1
      led0:
        voltage: 1000
        use_pulses: true
        frequency: 20
        duty_cycle: 50
```