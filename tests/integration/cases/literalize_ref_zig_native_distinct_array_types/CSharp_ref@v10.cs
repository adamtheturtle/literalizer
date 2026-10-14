class Check {
    public static void Main() {
var Shared = new int[] {
    1,
    2
};
var Second = new string[] {
    "one",
    "two"
};
var my_data = new object?[] {
    Shared,
    Second
};
    _ = my_data;
    }
}
