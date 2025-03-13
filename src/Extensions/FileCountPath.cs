using System;
using System.ComponentModel;
using System.Linq;
using System.Reactive.Linq;
using Bonsai;
using Bonsai.IO;

namespace Extensions
{
    [Combinator]
    [Description("Shuffles the input array.")]
    [WorkflowElementCategory(ElementCategory.Transform)]
    public class SuffixPath
    {
        public PathSuffix Suffix { get; set; }
        public IObservable<string> Process(IObservable<string> source)
        {
            return source.Select(input => PathHelper.AppendSuffix(input, Suffix));
        }
    }
}