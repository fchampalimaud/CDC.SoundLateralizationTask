# Fixation Time

As previously mentioned in the [state machine](state-machine.md#fixation-time) section, the fixation time precedes the stimulus presentation in which the animal is forced to stay in the CNP during this time, otherwise the trial will be aborted.

The fixation time can be modelled in different ways in different stages of training or according to different needs (for example, an optogenetics protocol may require the fixation time to be modelled differently). The section aims to explain how the fixation time works and how the user can modify its behavior.

## During the learning phase

When the animal is still learning the task (i.e. every training level except the last), the fixation time is modelled by the sum of a fixed duration and a random variable modeled by an exponential distribution.

$$t_\text{Fixation Time} = t_\text{Base Fixation} + (X ∼ \text{Exp}(\lambda))$$

Both $t_\text{Base Fixation}$ and $\lambda$ increase with training. $t_\text{Base Fixation}$ is incrementally increased every correct trial until it reaches a maximum value defined by the user, whereas the value of $\lambda$ is level-dependent.

## In the last level of training

When the animal reaches the final level of training, the user can model the fixation time as a sum of various distributions. At the moment, the distributions (and parameters) available are:
- Constant (fixed duration)
- Exponential Distribution
    - Mean ($\lambda$)
    - Maximum value
- Uniform Distribution
    - Lower limit
    - Upper limit
- Gaussian Distribution
    - Mean ($\mu$)
    - Standard Deviation ($\sigma$)
    - Minimum value
    - Maximum value

#### Example: Optogenetics

A use case that can take advantage of this feature is for when a user wants to run an optogenetics session in which the light turns on mid-fixation. A way to model the fixation time in this case could be by defining $t_\text{Opto Onset Time}$ - the time that goes from the beginning of the fixation and that ends when the optogenetics protocol starts - and $t_\text{Sound Onset Time}$ - the time that goes from start of the optogenetics protocol to the start of the stimulus - in a way that both of these components are given by:

$$t_\text{Opto Onset Time} = t_\text{Base Fix} + (X ∼ \text{Exp}(\lambda)) = t_\text{Sound Onset Time}$$

$$t_\text{Fixation Time} = t_\text{Opto Onset Time} + t_\text{Sound Onset Time}$$

The way to define this in the animal configuration file is the following:
```
fixation_time:
  training: # not used in the current example
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
```

Note that the user has to specify which distributions are going to be considered for the $t_\text{Opto Onset Time}$ by setting the parameter `opto_onset` to `true` for every distribution (the absence of this parameter is considered `false` by default).

### Catch trials

When the animal is in the last level of training, it's also possible to use the catch trials feature. This consists of defining a different set of distributions to model the intended fixation time in $p\%$ of the trials.

For example, if we want to model the fixation time as a sum of a fixed duration and a random variable modeled by an exponential distribution in 95% of the trials and a fixed duration in 5% of the trials, we can modify the animal configuration file as follows:
```
fixation_time:
  training: # not used in the current example
    min_value: 10
    delta: 1
    target: 200
  task:
    - distribution: constant
      value: 200
    - distribution: exponential
      mean: 400
      max_value: 2000
  catch_trials:
    probability: 0.05
    distribution:
      - distribution: constant
      value: 200
```