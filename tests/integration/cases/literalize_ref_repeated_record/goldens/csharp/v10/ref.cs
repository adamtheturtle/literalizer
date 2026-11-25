record Record0(int[] Value);
class Check {
    public static void Main() {
var Shared = new Record0(
    new int[] {
        1,
        2
    }
);
var my_data = new[] {
    Shared,
    Shared
};
    _ = my_data;
    }
}
