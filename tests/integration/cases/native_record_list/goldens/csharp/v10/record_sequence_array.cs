record Record1(int Age);
record Record0(string Name, bool Active, int Count, double Score, object? Missing, int[] Scores, Record1 Child);
class Check {
    public static void Main() {
var my_data = new[] {
    new Record0("Ada", true, 1, 1.5, (object?)null, new int[] {1, 2}, new Record1(3)),
    new Record0("Bob", false, 2, 2.5, (object?)null, new int[] {4}, new Record1(5))
};
    _ = my_data;
    }
}
