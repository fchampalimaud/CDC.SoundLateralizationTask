using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.IO;
using System.Linq;
using System.Reactive.Linq;
using Bonsai;
using Newtonsoft.Json;

namespace SLTFunctionality
{
    public class AnimalSpecificConfiguration
    {
        public int Animal { get; set; }
        public int Box { get; set; }
        public int Session { get; set; }
        public int SessionType { get; set; }
        public double[] ABLList { get; set; }
        public int CycleILD { get; set; }
        public double Bias { get; set; }
        public double BaseFixation {  get; set; }
        public double BaseFixationDelta { get; set; }
        public double BaseFixationTarget { get; set; }
        public double ExpFixationMean { get; set; }
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

    [Description("Generates an instance of the AnimalSpecificConfiguration class based on the JSON file containing the task's animal-specific configuration.")]
    [Combinator(MethodName = nameof(Generate))]
    [WorkflowElementCategory(ElementCategory.Source)]
    public class AnimalSpecificJSON
    {
        [Description("The name of the JSON file.")]
        [Editor(DesignTypes.OpenFileNameEditor, DesignTypes.UITypeEditor)]
        public String FilePath { get; set; }

        // Node version without input data stream
        public IObservable<AnimalSpecificConfiguration> Generate()
        {
            string fileContent = File.ReadAllText(FilePath);
            AnimalSpecificConfiguration asc = JsonConvert.DeserializeObject<AnimalSpecificConfiguration>(fileContent);

            return Observable.Defer(() => Observable.Return(asc));
        }

        // Node version with input data stream
        public IObservable<AnimalSpecificConfiguration> Generate<TSource>(IObservable<TSource> source)
        {
            string fileContent = File.ReadAllText(FilePath);
            AnimalSpecificConfiguration asc = JsonConvert.DeserializeObject<AnimalSpecificConfiguration>(fileContent);

            return source.Select(input => asc);
        }
    }
}
