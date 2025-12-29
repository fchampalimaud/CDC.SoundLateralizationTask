# Fixation Time
This is the state that precedes the stimulus presentation. The rodent must stay in the CNP during the entire time this state lasts so that the task progresses as expected, otherwise the trial is aborted. 

If the RandomizeFT setting is 1, the fixation time varies from trial to trial - it is randomly generated - in order to make the timing of the stimulus presentation (which happens as soon as the fixation time ends) unpredictable. In this case, the fixation time is given by:

$$t_{\text{Fix}} = t_{\text{Base Fix}} + (X ∼ \text{Exp}(λ))$$

If RandomizeFT is 0, the fixation time is only given by $t_{\text{Base Fix}}$.