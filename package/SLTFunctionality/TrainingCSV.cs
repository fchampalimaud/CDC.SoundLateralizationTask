using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Globalization;
using System.IO;
using System.Linq;
using System.Reactive.Linq;
using Bonsai;
using CsvHelper;

namespace SLTFunctionality
{
    public class TrainingConfiguration 
    {
        public int Level { get; set; }
        public int TrialsPerBlock { get; set; }
        public double FixedABL { get; set; }
        public int DifferentABLs { get; set; }
        public int ABLBlock { get; set; }
        public double ILDStepSize { get; set; }
        public int ILDSteps { get; set; }
        public int UseLog { get; set; }
        public double LogBase { get; set; }
        public double IntendedITI { get; set; }
        public int ITIReset { get; set; }
        public double MaxWait { get; set; }
        public int UseRT { get; set; }
        public int UseMaxRT { get; set; }
        public double MaxMT { get; set; }
        public double AbortPenalty { get; set; }
        public double IncorrectPenalty { get; set; }
        public double FixationAbortPenalty { get; set; }
        public int UsePerformance { get; set; }
        public double CriticalPerformance { get; set; }
        public int MaxAborts { get; set; }
        public int RepeatError { get; set; }
        public int RepeatAbort { get; set; }
        public int Speakers { get; set; }
        public int AbortLight { get; set; }
        public int ITILight { get; set; }
    }

    [Description("Generates an instance of the TrainingConfiguration class based on the row number of the CSV file containing the task's training matrix.")]
    [Combinator(MethodName = nameof(Generate))]
    [WorkflowElementCategory(ElementCategory.Source)]
    public class TrainingCSV
    {
        [Description("The name of the CSV file.")]
        [Editor(DesignTypes.OpenFileNameEditor, DesignTypes.UITypeEditor)]
        public String FileName { get; set; }
        [Description("The row number which corresponds to the desired training level (settings).")]
        [Editor(DesignTypes.NumericUpDownEditor, DesignTypes.UITypeEditor)]
        public int RowNumber { get; set; }

        TrainingConfiguration CSVtoArray()
        {
            using (var reader = new StreamReader(FileName))
            using (var csv = new CsvReader(reader, CultureInfo.InvariantCulture))
            {
                List<TrainingConfiguration> levels = csv.GetRecords<TrainingConfiguration>().ToList();

                if (RowNumber >= levels.Count) {
                    RowNumber = levels.Count - 1;
                } else if (RowNumber < 0) {
                    RowNumber = 0;
                }

                return levels[RowNumber];
            }
        }

        // Node version without input data stream
        public IObservable<TrainingConfiguration> Generate()
        {
            return Observable.Defer(() => Observable.Return(CSVtoArray()));
        }

        // Node version with input data stream
        public IObservable<TrainingConfiguration> Generate<TSource>(IObservable<TSource> source)
        {
            return source.Select(input => CSVtoArray());
        }
    }
}
