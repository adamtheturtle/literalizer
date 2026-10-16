record Record0(int X);
class Check {
    public static void Main() {
var my_data = new object?[] {
    new object?[] {new int[] {1}, new Record0(1)},
    new[] {new Record0(1), new Record0(2)},
    new[] {new Record0[] {}, new[] {new Record0(1)}},
    new object?[] {new object?[] {}, new object?[] {}}
};
    _ = my_data;
    }
}
