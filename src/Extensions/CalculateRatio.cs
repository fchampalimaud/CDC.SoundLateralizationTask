using System;
using System.ComponentModel;
using System.Linq;
using System.Reactive.Linq;
using Bonsai;
using PrintDict;

namespace Extensions
{
    [Combinator]
    [Description("Shuffles the input array.")]
    [WorkflowElementCategory(ElementCategory.Transform)]
    public class CalculateRatio
    {
        public IObservable<double> Process(IObservable<bool[]> source)
        {
            return source.Select(input =>
            {
                return input.Count(x => x == true)/(double)input.Length;
            });
        }
    }
}