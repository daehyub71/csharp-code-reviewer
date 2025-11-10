public class FileReader
{
    public string ReadFile(string path)
    {
        var reader = new StreamReader(path);
        var content = reader.ReadToEnd();
        return content;
    }
}
