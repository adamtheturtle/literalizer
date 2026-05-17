using System;
using System.Collections.Generic;
record Record0(string S, int I, double F, bool B, object N, DateOnly D, int Dt, string By);
class Check {
    public static void Main() {
var my_data = new Record0(
    "string",
    1,
    1.5,
    true,
    (object?)null,
    new DateOnly(2024, 1, 15),
    1705320000,
    "48656c6c6f"
);
    }
}
