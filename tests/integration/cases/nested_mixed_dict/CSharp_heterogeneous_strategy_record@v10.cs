using System.Collections.Generic;
record Record1(int A, string B, object C);
record Record0(Record1 Outer);
class Check {
    public static void Main() {
var my_data = new Record0(
    new Record1(
        1,
        "x",
        (object?)null
    )
);
    }
}
