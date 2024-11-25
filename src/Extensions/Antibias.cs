using Bonsai;
using System;
using System.ComponentModel;
using System.Collections.Generic;
using System.Linq;
using System.Reactive.Linq;

[Combinator]
[Description("")]
[WorkflowElementCategory(ElementCategory.Transform)]
public class Antibias
{
    double bias = 0.12;

    [Description("The threshold for starting biasing the reward (value between 0 and 1).")]
    [Editor(DesignTypes.NumericUpDownEditor, DesignTypes.UITypeEditor)]
    public double BiasThreshold 
    {
        get { return bias; }
        set { this.bias = value; } 
    }

    Tuple<double, double> getRewardBiases(Tuple<bool[], bool[]> history)
    {
        if (history.Item1.Length == history.Item2.Length)
        {
            double rightHit = 0;
            double leftHit = 0;
            for (int i = 0; i < history.Item1.Length; i++)
            {
                if (history.Item1[i] && history.Item2[i])
                {
                    leftHit++;
                } else if ((history.Item1[i] && !history.Item2[i])) {
                    rightHit++;
                }
            }

            if (Math.Abs((rightHit - leftHit) / history.Item1.Length) >= Math.Min(BiasThreshold, 1)) 
            {
                return new Tuple<double, double>(Math.Min(rightHit/leftHit, 4), Math.Min(leftHit/rightHit, 4));
            }
        }
        return new Tuple<double, double>(1, 1);
    }

    public IObservable<Tuple<double, double>> Process(IObservable<Tuple<bool[], bool[]>> source)
    {
        return source.Select(value => getRewardBiases(value));
    }
}
