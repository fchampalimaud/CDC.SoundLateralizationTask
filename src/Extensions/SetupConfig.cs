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
        /// <value>Property <c>Setup</c> is the ID number of the setup.</value>
        public int Setup { get; set; }
        /// <value>Property <c>LowToHighL</c> indicates whether the left poke is a low-to-high (true) or a high-to-low device.</value>
        public bool LowToHighL { get; set; }
        /// <value>Property <c>LowToHighCNP</c> indicates whether the central poke is a low-to-high (true) or a high-to-low device.</value>
        public bool LowToHighCNP { get; set; }
        /// <value>Property <c>LowToHighR</c> indicates whether the right poke is a low-to-high (true) or a high-to-low device.</value>
        public bool LowToHighR { get; set; }
        /// <value>Property <c>RewardOpenL</c> is the amount of time the left reward valve should be open (ms). This parameter is only relevant when the setup has uses valves instead of SyringePumps for reward delivery (i.e. <c>UsePumps</c> is 0).</value>
        public double RewardOpenL { get; set; }
        /// <value>Property <c>RewardOpenR</c> is the amount of time the right reward valve should be open (ms). This parameter is only relevant when the setup has uses valves instead of SyringePumps for reward delivery (i.e. <c>UsePumps</c> is 0).</value>
        public double RewardOpenR { get; set; }
        /// <value>Property <c>RightSlope</c> is the slope of the calibration curve of the right speaker. <b>StC</b></value>
        public double RightSlope { get; set; }
        /// <value>Property <c>RightIntercept</c> is the intercept of the calibration curve of the right speaker. <b>StC</b></value>
        public double RightIntercept { get; set; }
        /// <value>Property <c>LeftSlope</c> is the slope of the calibration curve of the left speaker. <b>StC</b></value>
        public double LeftSlope { get; set; }
        /// <value>Property <c>LeftIntercept</c> is the intercept of the calibration curve of the left speaker. <b>StC</b></value>
        public double LeftIntercept { get; set; }
        /// <value>Property <c>BoxLEDPeriod</c> is the period of the blinking of the Box LED (ms).</value>
        public double BoxLEDPeriod { get; set; }
        /// <value>Property <c>BoxLEDDutyCycle</c> is a value representing the proportion of time the LED is on when the Box LED is blinking. If it's 0 it means that the LED is always off, if it's 1 it means the LED is always on and, for example, if it's 0.5 it means that the LED is on half of the time and off for the remaining half.</value>
        public double BoxLEDDutyCycle { get; set; }
        /// <value>Property <c>PokeLEDPeriod</c> is the period of the blinking of the Central Poke LED (ms).</value>
        public double PokeLEDPeriod { get; set; }
        /// <value>Property <c>PokeLEDDutyCycle</c> is a value representing the proportion of time the LED is on when the Central Poke LED is blinking. If it's 0 it means that the LED is always off, if it's 1 it means the LED is always on and, for example, if it's 0.5 it means that the LED is on half of the time and off for the remaining half.</value>
        public double PokeLEDDutyCycle { get; set; }
        /// <value>Property <c>UsePumps</c> indicates whether the setup uses valves (false) or Harp SyringePumps (true) for reward delivery. <b>Add configuration parameters for the SyringePumps.</b></value>
        public bool UsePumps { get; set; }
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
    [Description("Generates an instance of the SetupConfig class based on the CSV file containing the task's setup-specific configuration.")]
    [WorkflowElementCategory(ElementCategory.Source)]
    /// <summary>
    /// Class <c>ReadSetupCSV</c> contains the logic of the Bonsai node with the same name.
    /// </summary>
    public class ReadSetupCSV
    {
        [Description("The name of the CSV file.")]
        [Editor(DesignTypes.OpenFileNameEditor, DesignTypes.UITypeEditor)]
        public String FilePath { get; set; }
        [Description("The row number which corresponds to the desired training level (settings).")]
        [Editor(DesignTypes.NumericUpDownEditor, DesignTypes.UITypeEditor)]
        public int RowNumber { get; set; }

        /// <summary>
        /// Reads a CSV file and outputs one of the rows.
        /// </summary>
        /// <returns>
        /// A <c>SetupConfig</c> instance corresponding to one of the rows of the CSV file.
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
