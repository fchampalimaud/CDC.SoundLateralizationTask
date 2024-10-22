using Bonsai;
using System;
using System.Globalization;
using System.ComponentModel;
using System.IO;
using System.Collections.Generic;
using System.Linq;
using System.Reactive.Linq;
using CsvHelper;

namespace Parameters
{
    /// <summary>
    /// Class <c>SetupConfig</c> models the input parameters of the Sound Lateralization Task present in the <c>setup.csv</c> file.
    /// </summary>
    public class SetupConfig
    {
        /// <value>Property <c>Setup</c> is the ID of the setup.</value>
        public int Setup { get; set; }
        /// <value>Property <c>LowToHighL</c> indicates whether the left poke is a low-to-high (true) or a high-to-low device.</value>
        public bool LowToHighL { get; set; }
        /// <value>Property <c>LowToHighCNP</c> indicates whether the central poke is a low-to-high (true) or a high-to-low device.</value>
        public bool LowToHighCNP { get; set; }
        /// <value>Property <c>LowToHighR</c> indicates whether the right poke is a low-to-high (true) or a high-to-low device.</value>
        public bool LowToHighR { get; set; }
        /// <value>Property <c>RewardOpenL</c> is the amount of time the left reward valve should be open (ms).</value>
        public double RewardOpenL { get; set; }
        /// <value>Property <c>RewardOpenR</c> is the amount of time the right reward valve should be open (ms).</value>
        public double RewardOpenR { get; set; }
        /// <value>Property <c>RightSlope</c> is the slope of the calibration curve of the right speaker.</value>
        public double RightSlope { get; set; }
        /// <value>Property <c>RightIntercept</c> is the intercept of the calibration curve of the right speaker.</value>
        public double RightIntercept { get; set; }
        /// <value>Property <c>LeftSlope</c> is the slope of the calibration curve of the left speaker.</value>
        public double LeftSlope { get; set; }
        /// <value>Property <c>LeftIntercept</c> is the intercept of the calibration curve of the left speaker.</value>
        public double LeftIntercept { get; set; }
        /// <value>Property <c>FlashPeriod</c></value>
        public double BoxLEDPeriod { get; set; }
        /// <value>Property <c>FlashPeriod</c></value>
        public double BoxLEDDutyCycle { get; set; }
        /// <value>Property <c>FlashPeriod</c></value>
        public double PokeLEDPeriod { get; set; }
        /// <value>Property <c>FlashPeriod</c></value>
        public double PokeLEDDutyCycle { get; set; }
        /// <value>Property <c>SoundDuration</c> is the duration of the sounds loaded to the soundcard (s).</value>
        // public double SoundDuration { get; set; }
        // public double PenaltyDurationPress { get; set; }
        // public double PenaltyFlashF { get; set; }
        // public double PerformAvg { get; set; }
        // public int IBILight { get; set; }
        // public int FS { get; set; }
        // public int FSDiv { get; set; }
        // public int FSSound { get; set; }
        // public int MinFreq { get; set; }
        // public int MaxFreq { get; set; }
        // public double RampTime { get; set; }
    }
}

namespace Extensions
{
    [Combinator]
    [Description("Generates an instance of the SetupConfig class based on the JSON file containing the task's setup-specific configuration.")]
    [WorkflowElementCategory(ElementCategory.Source)]
    // FIXME: rewrite function to ReadSetupCSV
    public class ReadSetupCSV
    {
        [Description("The name of the JSON file.")]
        [Editor(DesignTypes.OpenFileNameEditor, DesignTypes.UITypeEditor)]
        public String FilePath { get; set; }
        [Description("The row number which corresponds to the desired training level (settings).")]
        [Editor(DesignTypes.NumericUpDownEditor, DesignTypes.UITypeEditor)]
        public int RowNumber { get; set; }

        /// <summary>
        /// Reads a CSV file and outputs one of the rows.
        /// </summary>
        /// <returns>
        /// A <c>TrainingConfiguration</c> instance corresponding to one of the rows of the CSV file.
        /// </returns>
        Parameters.SetupConfig CSVtoArray()
        {
            using (var reader = new StreamReader(FilePath))
            using (var csv = new CsvReader(reader, CultureInfo.InvariantCulture))
            {
                List<Parameters.SetupConfig> setups = csv.GetRecords<Parameters.SetupConfig>().ToList();

                if (RowNumber >= setups.Count) {
                    RowNumber = setups.Count - 1;
                } else if (RowNumber < 0) {
                    RowNumber = 0;
                }

                return setups[RowNumber];
            }
        }

        public IObservable<Parameters.SetupConfig> Process()
        {
            return Observable.Defer(() => Observable.Return(CSVtoArray()));
        }

        public IObservable<Parameters.SetupConfig> Process<TSource>(IObservable<TSource> source)
        {
            return source.Select(input => CSVtoArray());
        }
    }
}
