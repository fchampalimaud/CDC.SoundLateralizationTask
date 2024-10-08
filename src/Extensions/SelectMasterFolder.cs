using Bonsai;
using System;
using System.ComponentModel;
using System.Collections.Generic;
using System.Linq;
using System.Reactive.Linq;

[Combinator]
[Description("")]
[WorkflowElementCategory(ElementCategory.Source)]
public class SelectMasterFolder
{
    [Description("The name of the JSON file.")]
    [Editor(DesignTypes.FolderNameEditor, DesignTypes.UITypeEditor)]
    public String FolderPath { get; set; }

    public IObservable<String> Process()
    {
        return Observable.Return(FolderPath);
    }
}
