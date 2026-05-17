using System.Collections.Generic;
record Record1(int Id, string Label);
record Record0(string Name, Record1[] Items);
class Check {
    public static void Main() {
var my_data = new Record0(
    "box",
    new[] {
        new Record1(
            1,
            "first"
        ),
        new Record1(
            2,
            "second"
        )
    }
);
    }
}
