using Bonsai;
using System;
using System.ComponentModel;
using System.Reactive.Linq;

namespace Extensions
{
    [Combinator]
    [Description("")]
    [WorkflowElementCategory(ElementCategory.Source)]
    public class GetOutputDir
    {
        [Description("The path to the output directory.")]
        [Editor(DesignTypes.FolderNameEditor, DesignTypes.UITypeEditor)]
        public String OutputDirPath { get; set; }

        public IObservable<String> Process()
        {
            return Observable.Return(OutputDirPath);
        }
    }
}