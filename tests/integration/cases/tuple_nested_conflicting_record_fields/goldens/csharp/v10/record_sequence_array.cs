record Record1(object[] Pair);
record Record0(Record1 Outer);
class Check {
    public static void Main() {
var my_data = new[] {
    new Record0(new Record1(new object[] {1, "first"})),
    new Record0(new Record1(new object[] {false, "second"}))
};
    _ = my_data;
    }
}
