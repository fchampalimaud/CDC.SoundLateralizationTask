using System;
using System.ComponentModel;
using System.Linq;
using System.Reactive.Linq;
using Bonsai;

namespace Extensions
{
    /// <summary>
    /// Class <c>ShuffleArray</c> contains the logic of the Bonsai node with the same name.
    /// </summary>
    [Combinator]
    [Description("Shuffles the input array.")]
    [WorkflowElementCategory(ElementCategory.Transform)]
    public class ShuffleArray
    {
        /// <summary>
        /// Shuffles the input array.
        /// </summary>
        /// <typeparam name="TSource">The type of the elements of the input array.</typeparam>
        /// <param name="source">the input data stream, which sends arrays of the type TSource.</param>
        /// <returns>
        /// The shuffled input array (of type TSource).
        /// </returns>
        public IObservable<TSource[]> Process<TSource>(IObservable<TSource[]> source)
        {
            return source.Select(input =>
            {
                Random random = new Random();
                return input.OrderBy(x => random.Next()).ToArray();
            });
        }
    }
}