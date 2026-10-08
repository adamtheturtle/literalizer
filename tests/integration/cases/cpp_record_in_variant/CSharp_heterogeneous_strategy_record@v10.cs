record Record1(bool[] K);
record Record0(object[] H);
class Check {
    public static void Main() {
var my_data = new Record0(
    new object[] {
        1,
        "a",
        new object[] {
            2,
            "b"
        },
        new Record1(
            new bool[] {
                true
            }
        )
    }
);
    }
}
