using System;
using System.ComponentModel;
using System.Linq;
using System.Reactive.Linq;
using Bonsai;

namespace CF
{
    /// <summary>
    /// Class <c>GenerateLateralizedILDsFL</c> contains the logic of the Bonsai node with the same name.
    /// </summary>
    [Description("Generates an array with the possible ILD values.")]
    [Combinator]
    [WorkflowElementCategory(ElementCategory.Source)]
    public class GenerateLateralizedILDsFL
    {
        double[] ilds;
        event Action<double[]> ValueChanged;

        [Description("The separation between two consecutive |ILD| values.")]
        public double[] ILDs
        {
            get { return ilds; }
            set
            {
                this.ilds = value;
                OnValueChanged(value);
            }
        }

        void OnValueChanged<T>(T value)
        {
            if (ValueChanged != null) {
                ValueChanged.Invoke(ILDArray());
            }
        }

        /// <summary>
        /// Generates an array containing the ILD values to be used based on <c>NumSteps</c>, <c>StepSize</c>, <c>UseLog</c> and <c>LogBase</c>.
        /// </summary>
        /// <returns>
        /// An array with <c>NumSteps</c> ILD values.
        /// </returns>
        double[] ILDArray()
        {
            double[] LateralizedILDs = new double[ILDs.Length * 2];
            for (int i = 0; i < ILDs.Length; i++)
            {
                LateralizedILDs[i] = - ILDs[ILDs.Length - 1 - i];
            }

            for (int i = ILDs.Length; i < ILDs.Length * 2; i++)
            {
                LateralizedILDs[i] = ILDs[i - ILDs.Length];
            }

            return LateralizedILDs;
        }

        /// <summary>
        /// Generates an observable sequence which outputs an array of ILDs. This method is called when the node doesn't have an input data stream.
        /// </summary>
        /// <returns>
        /// An observable sequence which sends a single event containing an array of ILD values.
        /// </returns>
        public IObservable<double[]> Process()
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
        public IObservable<double[]> Process<TSource>(IObservable<TSource> source)
        {
            return source.Select(input => ILDArray());
        }

    }
}
