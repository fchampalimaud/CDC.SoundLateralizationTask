using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Globalization;
using System.IO;
using System.Linq;
using System.Reactive.Linq;
using Bonsai;
using CsvHelper;

namespace SLTUtils
{
    /// <summary>
    /// Class <c>TrainingConfiguration</c> models the input parameters of the Sound Lateralization Task present in a row of the <c>training_settings.csv</c> file.
    /// </summary>
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

    /// <summary>
    /// Class <c>TrainingCSV</c> contains the logic of the Bonsai node with the same name.
    /// </summary>
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

        /// <summary>
        /// Reads a CSV file and outputs one of the rows.
        /// </summary>
        /// <returns>
        /// A <c>TrainingConfiguration</c> instance corresponding to one of the rows of the CSV file.
        /// </returns>
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

        /// <summary>
        /// Generates an observable sequence which outputs the training/task-specific parameters. This method is called when the node doesn't have an input data stream.
        /// </summary>
        /// <returns>
        /// An observable sequence which sends a single event containing a <c>TrainingConfiguration</c> instance.
        /// </returns>
        public IObservable<TrainingConfiguration> Generate()
        {
            return Observable.Defer(() => Observable.Return(CSVtoArray()));
        }

        /// <summary>
        /// Generates an observable sequence which outputs the training/task-specific parameters. This method is called when the node has an input data stream.
        /// </summary>
        /// <param name="source">the input data stream.</param>
        /// <returns>
        /// An observable sequence which sends a single event containing a <c>TrainingConfiguration</c> instance.
        /// </returns>
        public IObservable<TrainingConfiguration> Generate<TSource>(IObservable<TSource> source)
        {
            return source.Select(input => CSVtoArray());
        }
    }
}
