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
        /// <value>Property <c>Box</c> is the number of the box where the task was conducted.</value>
        public int Box { get; set; }
        /// <value>Property <c>Session</c> is the number of the session.</value>
        public int Session { get; set; }
        /// <value>Property <c>SessionType</c></value>
        public int SessionType { get; set; }
        /// <value>Property <c>SessionDuration</c> is the duration of the task ("hh:mm:ss").</value>
        public TimeSpan SessionDuration { get; set; }
        /// <value>Property <c>StartingTrialNumber</c> is the number of the first trial of the session.</value>
        public int StartingTrialNumber { get; set; }
        /// <value>Property <c>StartingBlockNumber</c> is the number of the first block of the session.</value>
        public int StartingBlockNumber { get; set; }
        /// <value>Property <c>StartingBlockNumber</c> is an array containing the possible ABLs to present when <c>DifferentABLs</c> is 1.</value>
        public double[] ABLList { get; set; }
        /// <value>Property <c>CycleILD</c></value>
        public int CycleILD { get; set; }
        /// <value>Property <c>Bias</c></value>
        public double Bias { get; set; }
        /// <value>Property <c>MinFT</c> is the minimum fixation time (ms).</value>
        public double MinFT{  get; set; }
        /// <value>Property <c>FTDelta</c> is the increment to make to the constant part of the fixation time every non-abort trial (ms).</value>
        public double FTDelta { get; set; }
        /// <value>Property <c>FTTarget</c> is the target value for the constant part of the fixation time (ms).</value>
        public double FTTarget { get; set; }
        /// <value>Property <c>ExpFTMean</c> is the mean value of the random part of the fixation time (ms).</value>
        public double ExpFTMean { get; set; }
        /// <value>Property <c>MinRT</c> is the minimum amount of time in CNP to wait after the sound presentation starts (s).</value>
        public double MinRT {  get; set; }
        /// <value>Property <c>RTDelta</c> is the increment to make to RT every non-abort trial (s).</value>
        public double RTDelta { get; set; }
        /// <value>Property <c>RTDelta</c> is the target value for RT (s).</value>
        public double RTTarget { get; set; }
        /// <value>Property <c>MaxRT</c> is the maximum amount of time in CNP to wait after sound presentation starts (s).</value>
        public double MaxRT { get; set; }
        /// <value>Property <c>MaxSamplingTime</c></value>
        public double[] MaxSamplingTime { get; set; }
        /// <value>Property <c>MinMT</c> is the minimum time allowed to move to LNP after leaving CNP (s).</value>
        public double MinMT { get; set; }
        /// <value>Property <c>MinLNP</c> is the minimum poke duration in LNP (s).</value>
        public double MinLNP { get; set; }
        /// <value>Property <c>LNPDelta</c> is the increment to make to LNP time every non-abort trial (s).</value>
        public double LNPDelta { get; set; }
        /// <value>Property <c>LNPTarget</c> is the target for LNP time (s).</value>
        public double LNPTarget { get; set; }
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
    }
}
