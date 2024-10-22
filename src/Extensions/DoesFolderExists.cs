using Bonsai;
using System;
using System.ComponentModel;
using System.IO;
using System.Collections.Generic;
using System.Linq;
using System.Reactive.Linq;

namespace Extensions
{
    [Combinator]
    [Description("Checks whether the folder already exists.")]
    [WorkflowElementCategory(ElementCategory.Transform)]
    public class DoesFolderExists
    {
        [Description("The path to the folder.")]
        [Editor(DesignTypes.FolderNameEditor, DesignTypes.UITypeEditor)]
        public string FolderPath { get; set; }

        bool doesFolderExists(string[] dirs)
        {
            for (int i = 0; i < dirs.Length; i++) {
                    if (dirs[i] == FolderPath) {
                        return true;
                    }
                }
                return false;
        }

        public IObservable<bool> Process(IObservable<string[]> source)
        {
            return source.Select(input => doesFolderExists(input));
        }
    }
}