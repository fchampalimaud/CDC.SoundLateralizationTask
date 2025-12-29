# Biased Blocks

This project allows for sessions in which there is a bias towards one of the sides in the presentation of stimuli.

These sessions, based on [[1](#references)], work as follows:

1. The first block of the session is an unbiased block with the number of trials given by the `trials_per_block` parameter of the `training.csv` file.

2. After the first block is completed, there is an equal probability that the first biased block is "leftward" or "rightward". The number of trials of this block is sampled from an exponential distribution clipped at a minimum and a maximum values, so that the hazard rate is almost flat.

3. After the first biased block ends, the preferential side switches (if it was left, it will be right in the next block, and vice-versa). The number of trials for this block is determined as described in 2. This logic is repeated until the end of the session.

## How to configure a biased blocks session?
To configure a biased blocks session, the `biased_session.is_biased_session` parameter of the `animal.yml` file must be set to `true`. Additionally, the remaining parameters related to this feature should be configured (see the following example).

```
biased_session:
  is_biased_session: true
  bias_probability: 0.8
  block_distributions:
    mean: 60
    min_value: 20
    max_value: 100
```

The `bias_probability` is the probability of one of the sides producing the most intense stimulus in a given block (in the next block, it will be the other way around). An example could be the left side being the correct answer 80% of the trials in a given block and the right side only 20%.

The `block_distributions` parameters model the (exponential) distribution from which the number of trials of a given biased block is sampled.

An example of an `animal.yml` file with the biased blocks session configured is shown below.

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
biased_session:
  is_biased_session: true
  bias_probability: 0.8
  block_distributions:
    mean: 60
    min_value: 20
    max_value: 100
```

## References

[1] J.-P. Noel et al., “A common computational and neural anomaly across mouse models of autism,” May 08, 2024, Neuroscience. doi: 10.1101/2024.05.08.593232.
