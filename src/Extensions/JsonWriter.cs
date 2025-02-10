using System.ComponentModel;
using Bonsai.IO;
using System.IO;

[Description("Writes a stream of serialized objects as Json objects to a single file.")]
public class JsonWriter : StreamSink<string, StreamWriter>
{

    protected override StreamWriter CreateWriter(Stream stream)
    {
        return new StreamWriter(stream);
    }

    protected override void Write(StreamWriter writer, string input)
    {
        writer.WriteLine(input);
    }
}
