#nullable enable annotations
class Check {
readonly object[] my_data = new object[] {
    1,
    "hello",
    true,
    (object?)null
};
    public static void Main() { }
    public void _Read_my_data() { _ = my_data; }
}
