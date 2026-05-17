using System.Collections.Generic;
record Record1(string Name, int Age);
record Record0(int Id, Record1 Owner);
class Check {
    public static void Main() {
var my_data = new Record0(
    1,
    new Record1(
        "Alice",
        30
    )
);
    }
}
