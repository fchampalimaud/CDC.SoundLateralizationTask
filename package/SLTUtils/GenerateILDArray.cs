using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Linq;
using System.Reactive.Linq;
using System.Threading;
using Bonsai;

namespace SLTUtils
{
    /// <summary>
    /// Class <c>GenerateILDArray</c> contains the logic of the Bonsai node with the same name.
    /// </summary>
    [Description("Generates an array with the possible ILD values.")]
    [Combinator(MethodName = nameof(Generate))]
    [WorkflowElementCategory(ElementCategory.Source)]
    public class GenerateILDArray
    {
        int numsteps;
        double stepsize;
        bool uselog;
        double logbase = Math.E;
        event Action<double[]> ValueChanged;

        [Description("The number of |ILD| values. The final array will contain 2*NumSteps elements, since it will contain both positive and negative ILD values.")]
        [Editor(DesignTypes.NumericUpDownEditor, DesignTypes.UITypeEditor)]
        public int NumSteps 
        { 
            get { return numsteps; }
            set
            {
                this.numsteps = value;
                OnValueChanged(value);
            } 
        }
        [Description("The separation between two consecutive |ILD| values.")]
        public double StepSize
        {
            get { return stepsize; }
            set
            {
                this.stepsize = value;
                OnValueChanged(value);
            }
        }
        [Description("Whether to use logarithmic steps between consecutive ILD values.")]
        public bool UseLog
        {
            get { return uselog; }
            set
            {
                this.uselog = value;
                OnValueChanged(value);
            }
        }
        [Description("The base of the logarithm.")]
        public double LogBase
        {
            get { return logbase; }
            set
            {
                this.logbase = value;
                OnValueChanged(value);
            }
        }

        void OnValueChanged<T>(T value)
        {
            ValueChanged?.Invoke(ILDArray());
        }

        /// <summary>
        /// Generates an array containing the ILD values to be used based on <c>NumSteps</c>, <c>StepSize</c>, <c>UseLog</c> and <c>LogBase</c>.
        /// </summary>
        /// <returns>
        /// An array with 2*<c>NumSteps</c> ILD values.
        /// </returns>
        double[] ILDArray()
        {
            double[] ILDs = new double[NumSteps * 2];
            for (int i = 0; i < NumSteps; i++)
            {
                if (UseLog)
                {
                    ILDs[i] = -StepSize * Math.Log(1 + NumSteps - i, LogBase);
                }
                else
                {
                    ILDs[i] = -StepSize * (NumSteps - i);
                }
            }

            for (int i = NumSteps; i < NumSteps * 2; i++)
            {
                if (UseLog)
                {
                    ILDs[i] = StepSize * Math.Log(1 + i - NumSteps + 1, LogBase);
                }
                else
                {
                    ILDs[i] = StepSize * (i - NumSteps + 1);
                }
            }

            return ILDs;
        }

        /// <summary>
        /// Generates an observable sequence which outputs an array of ILDs. This method is called when the node doesn't have an input data stream.
        /// </summary>
        /// <returns>
        /// An observable sequence which sends a single event containing an array of ILD values.
        /// </returns>
        public IObservable<double[]> Generate()
        {
            return Observable
                .Defer(() => Observable.Return(ILDArray()))
                .Concat(Observable.FromEvent<double[]>(
                    handler => ValueChanged += handler,
                    handler => ValueChanged -= handler));
        }

        // Node version with input data stream
        /// <summary>
        /// Generates an observable sequence which outputs an array of ILDs. This method is called when the node has an input data stream.
        /// </summary>
        /// <param name="source">the input data stream.</param>
        /// <returns>
        /// An observable sequence which sends a single event containing an array of ILD values.
        /// </returns>
        public IObservable<double[]> Generate<TSource>(IObservable<TSource> source)
        {
            return source.Select(input => ILDArray());
        }

    }
}
