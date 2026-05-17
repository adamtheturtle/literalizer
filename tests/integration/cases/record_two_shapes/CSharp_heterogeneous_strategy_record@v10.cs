using System.Collections.Generic;
record Record1(int Count, int Rate);
record Record2(int Retries, int Timeout);
record Record0(Record1 Metrics, Record2 Flags);
class Check {
    public static void Main() {
var my_data = new Record0(
    new Record1(
        100,
        50
    ),
    new Record2(
        3,
        30
    )
);
    }
}
