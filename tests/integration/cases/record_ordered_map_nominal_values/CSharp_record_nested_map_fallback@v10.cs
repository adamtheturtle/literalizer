using System.Collections.Generic;
record Record1(int X);
record Record0(Dictionary<string, object> Values, bool Flag);
class Check {
    public static void Main() {
var my_data = new Record0(
    new Dictionary<string, object> {
        ["first"] = new Record1(
            1
        ),
        ["second"] = new Record1(
            2
        )
    },
    true
);
    }
}
