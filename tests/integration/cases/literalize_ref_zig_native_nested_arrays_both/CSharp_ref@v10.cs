class Check {
    public static void Main() {
var Shared = new int[] {
    1,
    2
};
var Second = new int[] {
    3,
    4
};
var my_data = new int[][] {
    Shared,
    Second
};
my_data = new int[][] {
    Shared,
    Second
};
    _ = my_data;
    }
}
