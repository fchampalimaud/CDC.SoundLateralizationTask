using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Linq;
using System.Reactive.Linq;
using Bonsai;

namespace SLTUtils
{
    [Combinator]
    [Description("Shuffles the input array.")]
    [WorkflowElementCategory(ElementCategory.Transform)]
    public class ShuffleArray
    {
        public IObservable<TSource[]> Process<TSource>(IObservable<TSource[]> source)
        {
            return source.Select(input =>
            {
                Random random = new Random();
                TSource[] output = input.OrderBy(x => random.Next()).ToArray();
                return output;
            });
        }
    }
}
