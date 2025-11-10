public class UserService
{
    public void ProcessData(string data)
    {
        var result = data.ToUpper();
        Console.WriteLine(result);
    }
}
