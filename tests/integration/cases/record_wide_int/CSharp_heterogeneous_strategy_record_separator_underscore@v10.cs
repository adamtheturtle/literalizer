using System.Collections.Generic;
record Record0(int Quantity, ulong Big, double Ratio, string Label, bool Ok);
class Check {
    public static void Main() {
var my_data = new Record0(
    1_000_000,
    18_446_744_073_709_551_615,
    2.5,
    "tag",
    true
);
    }
}
