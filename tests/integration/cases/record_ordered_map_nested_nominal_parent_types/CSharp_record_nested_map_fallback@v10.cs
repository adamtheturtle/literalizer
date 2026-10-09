using System.Collections.Generic;
record Record2(int X);
record Record1(Dictionary<string, object> Values, bool Flag);
record Record3(string Y);
record Record0(Record1 First, Record1 Second);
class Check {
    public static void Main() {
var my_data = new Record0(
    new Record1(
        new Dictionary<string, object> {
            ["outer"] = new Dictionary<string, object> {
                ["inner"] = new Record2(
                    1
                )
            }
        },
        true
    ),
    new Record1(
        new Dictionary<string, object> {
            ["outer"] = new Dictionary<string, object> {
                ["inner"] = new Record3(
                    "s"
                )
            }
        },
        false
    )
);
    }
}
