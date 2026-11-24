record Record0(int Field);
class Check {
    public static void Main() {
var Value = new Record0(
    2
);
var my_data = new[] {
    new Record0(1),
    Value
};
    _ = my_data;
    }
}
