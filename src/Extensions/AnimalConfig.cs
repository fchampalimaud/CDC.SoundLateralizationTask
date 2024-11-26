using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.IO;
using System.Linq;
using System.Reactive.Linq;
using Bonsai;
using Newtonsoft.Json;

namespace Parameters
{
    /// <summary>
    /// Class <c>AnimalConfig</c> models the input parameters of the Sound Lateralization Task present in the <c>animal.json</c> file.
    /// </summary>
    public class AnimalConfig
    {
        /// <value>Property <c>Animal</c> is the ID number of the animal.</value>
        public int Animal { get; set; }
        /// <value>Property <c>Box</c> is the number of the box where the task is going to be conducted.</value>
        public int Box { get; set; }
        /// <value>Property <c>Session</c> is the number of the session.</value>
        public int Session { get; set; }
        /// <value>Property <c>SessionType</c> is the number of the session type (for example, the "standard" sound lateralization task might be session type number 1 and a version of the task with optogenetics might be session type number 2). This parameter is purely informative, it doesn't change how the task works by itself.</value>
        public int SessionType { get; set; }
        /// <value>Property <c>SessionDuration</c> is the duration of the task (in the format "hh:mm:ss").</value>
        public TimeSpan SessionDuration { get; set; }
        /// <value>Property <c>StartingTrialNumber</c> is the number of the first trial of the session. <b>At the moment, this parameter is not updated automatically, but it should be in the future.</b></value>
        public int StartingTrialNumber { get; set; }
        /// <value>Property <c>StartingBlockNumber</c> is the number of the first block of the session. <b>At the moment, this parameter is not updated automatically, but it should be in the future.</b></value>
        public int StartingBlockNumber { get; set; }
        /// <value>Property <c>ABLList</c> is an array containing the possible ABLs to present when the <c>DifferentABLs</c> parameter from the <c>training.csv</c> file is not 0.</value>
        public double[] ABLList { get; set; }
        /// <value>If the <c>CycleILD</c> property is false, an ILD value is randomly picked every trial from the array of ILDs. Otherwise, the ILD array is shuffled and the ILD is picked by just following the new array order; when the end of the array is reached, the array is shuffled again and the procedure is repeated.</value>
        public bool CycleILD { get; set; }
        public int[] SoundIndexes { get; set; }
        /// <value>Property <c>Bias</c> indicates whether the probability of the louder side being left or right is biased or not. If the value is less than 0.5, there's a bigger probability of the louder side being left, if it's greater than 0.5, there's a bigger probability of being right. If it's equal to 0.5, there's no bias. <b>NOT IMPLEMENTED!</b></value>
        public double Bias { get; set; }
        public double MinLEDOnset{  get; set; }
        public double LEDOnsetDelta { get; set; }
        public double LEDOnsetTarget { get; set; }
        public double ExpLEDOnset { get; set; }
        /// <value>Property <c>MinFT</c> is the starting value for the constant part of the fixation time (ms). <b>At the moment, this parameter is not updated automatically, but it should be asked whether it should be updated in the future.</b></value>
        public double MinFT{  get; set; }
        /// <value>Property <c>FTDelta</c> is the increment to make to the constant part of the fixation time every non-abort trial (ms).</value>
        public double FTDelta { get; set; }
        /// <value>Property <c>FTTarget</c> is the target value for the constant part of the fixation time (ms).</value>
        public double FTTarget { get; set; }
        /// <value>Property <c>ExpFTMean</c> is the mean value of the random part of the fixation time (ms), which follows an exponential distribution.</value>
        public double ExpFTMean { get; set; }
        /// <value>Property <c>MinRT</c> is the minimum amount of time the animal has to wait in the CNP after the sound presentation starts (s). This parameter aims to avoid that the animal "reacts" before the stimulus is presented.</value>
        public double MinRT {  get; set; }
        /// <value>Property <c>RTDelta</c> is the increment to make to RT every non-abort trial (s). <b>Ask if this should be applied to MinRT or MaxRT and why.</b></value>
        public double RTDelta { get; set; }
        /// <value>Property <c>RTDelta</c> is the target value for RT (s). <b>Ask if this should be applied to MinRT or MaxRT and why.</b></value>
        public double RTTarget { get; set; }
        /// <value>Property <c>MaxRT</c> is the maximum amount of time the animal has to wait in the CNP after the sound presentation starts (s). <b>It should be related to the duration of the noises present, although currently this is not the case.</b></value>
        public double MaxRT { get; set; }
        /// <value>Property <c>MaxSamplingTime</c> <b>NOT IMPLEMENTED!</b></value>
        public double[] MaxSamplingTime { get; set; }
        /// <value>Property <c>MinMT</c> is the minimum time allowed for the animal to move to one of the LNPs after leaving the CNP (s). This parameter aims to "catch" possible "ghost" pokes (hardware faults).</value>
        public double MinMT { get; set; }
        /// <value>Property <c>MinLNP</c> is the minimum amount of time the animal has to keep poking the LNP for the reward to be given when the answer is correct (s). <b>At the moment, if LNPTime is less than MinLNP the trial still counts as successful but the animal doesn't get a reward. In the future, this should be considered an abort instead.</b></value>
        public double MinLNP { get; set; }
        /// <value>Property <c>LNPDelta</c> is the increment to make to LNP time every non-abort trial (s).</value>
        public double LNPDelta { get; set; }
        /// <value>Property <c>LNPTarget</c> is the target for LNP time (s).</value>
        public double LNPTarget { get; set; }
        /// <value>Property <c>BaseReward</c> is the amount of reward the animal receives when answers correctly (uL).</value>
        public double BaseReward { get; set; }
        /// <value>Property <c>OptoSession</c> is whether the current session is using optogenetics.</value>
        public bool OptoSession { get; set; }
        /// <value>Property <c>OptoContinuous</c> is whether the optogenetics session uses a continuous emission of light (true) or if it emits in small pulses with a certain frequency.</value>
        public bool OptoContinuous { get; set; }
        /// <value>Property <c>OptoRamp</c> is the ramp time of the LED (ms).</value>
        public double OptoRamp { get; set; }
        /// <value>Property <c>OptoTime</c> is the maximum time the LED stays on in a single emission (s). It only works when <c>OptoContinuous</c> is true.</value>
        public double OptoTime { get; set; }
        /// <value>Property <c>OptoFrequency</c> is the frequency with which the LED emits pulses of light. It only works when <c>OptoContinuous</c> is false.</value>
        public double OptoFrequency { get; set; }
        /// <value>Property <c>OptoPulseDuration</c> is the duration of a single pulse (ms). It only works when <c>OptoContinuous</c> is false.</value>
        public double OptoPulseDuration { get; set; }
        public bool AutobiasCorrection { get; set; }
    }
}

namespace Extensions
{
    /// <summary>
    /// Class <c>ReadAnimalJSON</c> contains the logic of the Bonsai node with the same name.
    /// </summary>
    [Description("Generates an instance of the AnimalConfig class based on the JSON file containing the task's animal-specific configuration.")]
    [Combinator]
    [WorkflowElementCategory(ElementCategory.Source)]
    public class ReadAnimalJSON
    {
        [Description("The name of the JSON file.")]
        [Editor(DesignTypes.OpenFileNameEditor, DesignTypes.UITypeEditor)]
        public String FilePath { get; set; }

        /// <summary>
        /// Reads the animal-specific input parameters needed for the Sound Lateralization Task from a JSON file.
        /// </summary>
        /// <returns>
        /// An observable sequence which sends a single event containing an <c>AnimalConfig</c> instance.
        /// </returns>
        public IObservable<Parameters.AnimalConfig> Process()
        {
            string fileContent = File.ReadAllText(FilePath);
            Parameters.AnimalConfig animalConfig = JsonConvert.DeserializeObject<Parameters.AnimalConfig>(fileContent);

            return Observable.Defer(() => Observable.Return(animalConfig));
        }

        /// <summary>
        /// Reads the animal-specific input parameters needed for the Sound Lateralization Task from a JSON file.
        /// </summary>
        /// <returns>
        /// An observable sequence which sends a single event containing an <c>AnimalConfig</c> instance.
        /// </returns>
        public IObservable<Parameters.AnimalConfig> Process<TSource>(IObservable<TSource> source)
        {
            string fileContent = File.ReadAllText(FilePath);
            Parameters.AnimalConfig animalConfig = JsonConvert.DeserializeObject<Parameters.AnimalConfig>(fileContent);

            return source.Select(input => animalConfig);
        }
    }
}
