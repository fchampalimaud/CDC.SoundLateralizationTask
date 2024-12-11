﻿using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Globalization;
using System.IO;
using System.Linq;
using System.Reactive.Linq;
using Bonsai;
using CsvHelper;

namespace Parameters
{
    /// <summary>
    /// Class <c>TrainingConfig</c> models the input parameters of the Sound Lateralization Task present in a row of the <c>training_settings.csv</c> file.
    /// </summary>
    public class TrainingConfig
    {
        /// <value>Property <c>Level</c> is the number of the level.</value>
        public int Level { get; set; }
        /// <value>Property <c>TrialsPerBlock</c> is the number of trials that a block of the current level has.</value>
        public int TrialsPerBlock { get; set; }
        /// <value>Property <c>FixedABL</c> is the ABL value to use when the <c>DifferentABLs</c> property is 0.</value>
        public double FixedABL { get; set; }
        /// <value>Property <c>DifferentABLs</c> is whether to use the ABLs from <c>ABLList</c> (1) or from <c>FixedABL</c> (0).</value>
        public bool DifferentABLs { get; set; }
        /// <value>Property <c>ABLBlock</c> is whether ABLs change only across blocks (1) or not (0).</value>
        public bool ABLBlock { get; set; }
        /// <value>Property <c>ILDStepSize</c> is the separation between two consecutive |ILD| values.</value>
        public double ILDStepSize { get; set; }
        /// <value>Property <c>ILDSteps</c> is the number of |ILD| values. The final array will contain 2*<c>ILDSteps</c> elements to account for both the positive and the negative ILD values.</value>
        public int ILDSteps { get; set; }
        /// <value>Property <c>UseLog</c> is whether to use logarithmic steps between consecutive ILD values.</value>
        public bool UseLog { get; set; }
        /// <value>Property <c>LogBase</c> is the base of the logarithm.</value>
        public double LogBase { get; set; }
        /// <value>Property <c>IntendedITI</c> is the intended ITI duration (s).</value>
        public double IntendedITI { get; set; }
        /// <value>Property <c>ITIReset</c> is whether the ITI partially resets if the animal tries to poke in the CNP before it ends.</value>
        public bool ITIReset { get; set; }
        /// <value>Property <c>MaxWait</c> is the maximum allowed time to start the trial (s).</value>
        public double MaxWait { get; set; }
        /// <value>Property <c>OptoExpMean</c></value>
        public double OptoExpMean { get; set; }
        /// <value>Property <c>SoundExpMean</c></value>
        public double SoundExpMean { get; set; }
        /// <value>Property <c>UseRT</c> is whether the sound stops with the animal leaving the CNP.</value>
        public bool UseRT { get; set; }
        /// <value>Property <c>UseMaxRT</c> is whether there is a MaxRT. <b>Note: I don't know what is supposed to happen when there's no MaxRT.</b></value>
        public bool UseMaxRT { get; set; }
        /// <value>Property <c>MaxMT</c> is the maximum allowed time to move to the LNP (s).</value>
        public double MaxMT { get; set; }
        /// <value>Property <c>AbortPenalty</c> is the abort penalty time (s).</value>
        public double AbortPenalty { get; set; }
        /// <value>Property <c>IncorrectPenalty</c> is the incorrect answer penalty time (s).</value>
        public double IncorrectPenalty { get; set; }
        /// <value>Property <c>FixationAbortPenalty</c> is the fixation abort penalty time (s).</value>
        public double FixationAbortPenalty { get; set; }
        /// <value>Property <c>UsePerformance</c> is whether there is a minimum performance requirement to advance to the next block.</value>
        public bool UsePerformance { get; set; }
        /// <value>Property <c>CriticalPerformance</c> is the minimum correct answer ratio required to advance block (if <c>UsePerformance</c> is 1).</value>
        public double CriticalPerformance { get; set; }
        /// <value>Property <c>MaxAborts</c> <b>NOT IMPLEMENTED!</b></value>
        public int MaxAborts { get; set; }
        /// <value>Property <c>RepeatError</c> is whether the stimulus is repeated after incorrect responses.</value>
        public int RepeatError { get; set; }
        /// <value>Property <c>RepeatAbort</c> is whether the stimulus is repeated after aborts.</value>
        public int RepeatAbort { get; set; }
        /// <value>Property <c>Speakers</c> is whether the animal is using headphones or not (Headphones = 1, Box Speakers = 0). <b>At the moment, this parameter doesn't modify the behavior of the task. Perhaps in the future, it might be possible to input the calibration curves of both the box speakers and the headphones so that this parameter switches to the correct calibration curves.</b></value>
        public bool Speakers { get; set; }
        /// <value>Property <c>AbortLight</c> is whether the Box LED should blink during the abort penalty time (1) or not (0).</value>
        public bool AbortLight { get; set; }
        /// <value>Property <c>ITILight</c> is whether the Box LED should turn on during the ITI (1) or not (0).</value>
        public bool ITILight { get; set; }
        /// <value>Property <c>PokeLight</c> is whether the CNP LED should turn on when the new trial is ready (1) or not (0).</value>
        public bool PokeLight { get; set; }
        /// <value>Property <c>FixLight</c> is whether the CNP LED should blink during the fixation time (1) or not (0).</value>
        public bool FixLight { get; set; }
    }
}

namespace Extensions
{
    /// <summary>
    /// Class <c>ReadTrainingCSV</c> contains the logic of the Bonsai node with the same name.
    /// </summary>
    [Description("Generates an instance of the TrainingConfiguration class based on the row number of the CSV file containing the task's training matrix.")]
    [Combinator]
    [WorkflowElementCategory(ElementCategory.Source)]
    public class ReadTrainingCSV
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
        /// A <c>TrainingConfiguration</c> instance corresponding to one of the rows of the CSV file.
        /// </returns>
        Tuple<Parameters.TrainingConfig, int> CSVtoArray()
        {
            using (var reader = new StreamReader(FilePath))
            using (var csv = new CsvReader(reader, CultureInfo.InvariantCulture))
            {
                List<Parameters.TrainingConfig> levels = csv.GetRecords<Parameters.TrainingConfig>().ToList();

                if (RowNumber >= levels.Count) {
                    RowNumber = levels.Count - 1;
                } else if (RowNumber < 0) {
                    RowNumber = 0;
                }

                return new Tuple<Parameters.TrainingConfig, int>(levels[RowNumber], levels.Count);
            }
        }

        /// <summary>
        /// Generates an observable sequence which outputs the training/task-specific parameters. This method is called when the node doesn't have an input data stream.
        /// </summary>
        /// <returns>
        /// An observable sequence which sends a single event containing a <c>TrainingConfiguration</c> instance.
        /// </returns>
        public IObservable<Tuple<Parameters.TrainingConfig, int>> Process()
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
        public IObservable<Tuple<Parameters.TrainingConfig, int>> Process<TSource>(IObservable<TSource> source)
        {
            return source.Select(input => CSVtoArray());
        }
    }
}
