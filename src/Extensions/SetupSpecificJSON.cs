using Bonsai;
using System;
using System.ComponentModel;
using System.IO;
using System.Collections.Generic;
using System.Linq;
using System.Reactive.Linq;
using Newtonsoft.Json;

/// <summary>
/// Class <c>SetupSpecificConfiguration</c> models the input parameters of the Sound Lateralization Task present in the <c>setup_settings.json</c> file.
/// </summary>
public class SetupSpecificConfiguration
{
    /// <value>Property <c>LowToHighL</c> indicates whether the left poke is a low-to-high (true) or a high-to-low device.</value>
    public bool LowToHighL { get; set; }
    /// <value>Property <c>LowToHighCNP</c> indicates whether the central poke is a low-to-high (true) or a high-to-low device.</value>
    public bool LowToHighCNP { get; set; }
    /// <value>Property <c>LowToHighR</c> indicates whether the right poke is a low-to-high (true) or a high-to-low device.</value>
    public bool LowToHighR { get; set; }
    /// <value>Property <c>RewardOpenL</c> is the amount of time the left reward valve should be open (ms).</value>
    public double RewardOpenL { get; set; }
    /// <value>Property <c>RewardOpenR</c> is the amount of time the right reward valve should be open (ms).</value>
    public double RewardOpenR { get; set; }
    /// <value>Property <c>RightSlope</c> is the slope of the calibration curve of the right speaker.</value>
    public double RightSlope { get; set; }
    /// <value>Property <c>RightIntercept</c> is the intercept of the calibration curve of the right speaker.</value>
    public double RightIntercept { get; set; }
    /// <value>Property <c>LeftSlope</c> is the slope of the calibration curve of the left speaker.</value>
    public double LeftSlope { get; set; }
    /// <value>Property <c>LeftIntercept</c> is the intercept of the calibration curve of the left speaker.</value>
    public double LeftIntercept { get; set; }
    /// <value>Property <c>SoundDuration</c> is the duration of the sounds loaded to the soundcard (s).</value>
    public double SoundDuration { get; set; }
    public double PenaltyDurationPress { get; set; }
    public double PenaltyFlashF { get; set; }
    public double PerformAvg { get; set; }
    public int IBILight { get; set; }
    public int FS { get; set; }
    public int FSDiv { get; set; }
    public int FSSound { get; set; }
    public int MinFreq { get; set; }
    public int MaxFreq { get; set; }
    public double RampTime { get; set; }
}

[Combinator]
[Description("Generates an instance of the SetupSpecificConfiguration class based on the JSON file containing the task's setup-specific configuration.")]
[WorkflowElementCategory(ElementCategory.Source)]
public class SetupSpecificJSON
{
    [Description("The name of the JSON file.")]
    [Editor(DesignTypes.OpenFileNameEditor, DesignTypes.UITypeEditor)]
    public String FilePath { get; set; }

    public IObservable<SetupSpecificConfiguration> Process()
    {
        string fileContent = File.ReadAllText(FilePath);
        SetupSpecificConfiguration ssc = Newtonsoft.Json.JsonConvert.DeserializeObject<SetupSpecificConfiguration>(fileContent);

        return Observable.Defer(() => Observable.Return(ssc));
    }
}
