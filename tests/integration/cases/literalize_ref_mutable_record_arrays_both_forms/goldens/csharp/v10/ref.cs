record Record0(int Id);
class Check {
    public static void Main() {
var Shared = new[] {
    new Record0(1)
};
var Second = new[] {
    new Record0(2)
};
var my_data = new[] {
    Shared,
    Second
};
my_data = new[] {
    Shared,
    Second
};
    _ = my_data;
    }
}
