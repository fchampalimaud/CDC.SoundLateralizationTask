using Bonsai;
using System;
using System.ComponentModel;
using System.Collections.Generic;
using System.Linq;
using System.Reactive.Linq;
using Newtonsoft.Json;
using System.IO;

namespace Extensions
{
    /// <summary>
    /// Class <c>StartupFile</c> contains the relevant paths used during the Sound Lateralization Task which are read from the <c>startup.json</c> file. This is the only file which is hardcoded both in the Bonsai and in the Python projects, i.e. this file can't be moved from its current location and its name can't be changed. It's not recommended that relative paths are used, but keep in mind that in case one wants to, the relative paths must be relative to the <c>./src</c> (where the <c>.</c> is the root directory of the project).
    /// </summary>
    public class StartupFile
    {
        /// <value>Property <c>SetupFile</c> is the path to the <c>setup.csv</c> file.</value>
        public string SetupFile { get; set; }
        /// <value>Property <c>TrainingFile</c> is the path to the <c>training.csv</c> file.</value>
        public string TrainingFile { get; set; }
        /// <value>Property <c>AnimalFile</c> is the path to the <c>animal.json</c> file.</value>
        public string AnimalFile { get; set; }
        /// <value>Property <c>OutputDir</c> is the path to the output directory.</value>
        public string OutputDir { get; set; }
    }

    /// <summary>
    /// Class <c>ReadStartupFile</c> contains the logic of the Bonsai node with the same name.
    /// </summary>
    [Combinator]
    [Description("")]
    [WorkflowElementCategory(ElementCategory.Source)]
    public class ReadStartupFile
    {
        [Description("The name of the JSON file.")]
        [Editor(DesignTypes.OpenFileNameEditor, DesignTypes.UITypeEditor)]
        public String FilePath { get; set; }

        /// <summary>
        /// Reads the startup input parameters needed for the Sound Lateralization Task from a JSON file.
        /// </summary>
        /// <returns>
        /// An observable sequence which sends a single event containing a <c>StartupFile</c> instance.
        /// </returns>
        public IObservable<StartupFile> Process()
        {
            string fileContent = File.ReadAllText(FilePath);
            StartupFile startup = JsonConvert.DeserializeObject<StartupFile>(fileContent);
            return Observable.Defer(() => Observable.Return(startup));
        }
    }
}
