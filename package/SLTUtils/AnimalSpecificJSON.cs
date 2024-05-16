using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.IO;
using System.Linq;
using System.Reactive.Linq;
using Bonsai;
using Newtonsoft.Json;

namespace SLTUtils
{
    /// <summary>
    /// Class <c>AnimalSpecificConfiguration</c> models the input parameters of the Sound Lateralization Task present in the <c>animal_settings.json</c> file.
    /// </summary>
    public class AnimalSpecificConfiguration
    {
        public int Animal { get; set; }
        public int Box { get; set; }
        public int Session { get; set; }
        public int SessionType { get; set; }
        public TimeSpan SessionDuration { get; set; }
        public int StartingTrialNumber { get; set; }
        public int StartingBlockNumber { get; set; }
        public double[] ABLList { get; set; }
        public int CycleILD { get; set; }
        public double Bias { get; set; }
        public double MinFT{  get; set; }
        public double FTDelta { get; set; }
        public double FTTarget { get; set; }
        public double ExpFTMean { get; set; }
        public double MinRT {  get; set; }
        public double RTDelta { get; set; }
        public double RTTarget { get; set; }
        public double MaxRT { get; set; }
        public double[] MaxSamplingTime { get; set; }
        public double MinMT { get; set; }
        public double MinLNP { get; set; }
        public double LNPDelta { get; set; }
        public double LNPTarget { get; set; }
        //public double PenaltyDurationPress { get; set; }
        //public double PenaltyFlashF { get; set; }
        //public double PerformAvg { get; set; }
        //public int FS { get; set; }
        //public int FSDiv { get; set; }
        //public int FSSound { get; set; }
        //public int FreqMin { get; set; }
        //public int FreqMax { get; set; }
        //public double RampTime { get; set; }
        //public double SoundDuration { get; set; }
        //public int IBILight { get; set; }
        //public double Rp1 { get; set; }
        //public double Rp2 { get; set; }
        //public int[] RCalFactor { get; set; }
        //public int[] RVecCal { get; set; }
        //public double Lp1 { get; set; }
        //public double Lp2 { get; set; }
        //public int[] LCalFactor { get; set; }
        //public int[] LVecCal { get; set; }
        //public double RewardOpenL { get; set; }
        //public double RewardOpenR { get; set; }
    }

    /// <summary>
    /// Class <c>AnimalSpecificJSON</c> contains the logic of the Bonsai node with the same name.
    /// </summary>
    [Description("Generates an instance of the AnimalSpecificConfiguration class based on the JSON file containing the task's animal-specific configuration.")]
    [Combinator(MethodName = nameof(Generate))]
    [WorkflowElementCategory(ElementCategory.Source)]
    public class AnimalSpecificJSON
    {
        [Description("The name of the JSON file.")]
        [Editor(DesignTypes.OpenFileNameEditor, DesignTypes.UITypeEditor)]
        public String FilePath { get; set; }

        /// <summary>
        /// Reads the animal-specific input parameters needed for the Sound Lateralization Task from a JSON file.
        /// </summary>
        /// <returns>
        /// An observable sequence which sends a single event containing an <c>AnimalSpecificConfiguration</c> instance.
        /// </returns>
        public IObservable<AnimalSpecificConfiguration> Generate()
        {
            string fileContent = File.ReadAllText(FilePath);
            AnimalSpecificConfiguration asc = JsonConvert.DeserializeObject<AnimalSpecificConfiguration>(fileContent);

            return Observable.Defer(() => Observable.Return(asc));
        }
    }
}
