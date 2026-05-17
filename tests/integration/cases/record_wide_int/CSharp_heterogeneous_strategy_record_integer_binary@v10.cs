using System.Collections.Generic;
record Record0(int Quantity, ulong Big, double Ratio, string Label, bool Ok);
class Check {
    public static void Main() {
var my_data = new Record0(
    0b11110100001001000000,
    0b1111111111111111111111111111111111111111111111111111111111111111,
    2.5,
    "tag",
    true
);
    }
}
