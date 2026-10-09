using System.Collections.Generic;
record Record1(int X);
record Record0(Dictionary<string, object> Values, bool Flag);
class Check {
    public static void Main() {
var my_data = new Record0(
    new Dictionary<string, object> {
        ["entries"] = new object[] {
            new Dictionary<string, object> {
                ["inner"] = new Record1(
                    1
                )
            },
            new Dictionary<string, object> {
                ["inner"] = new Record1(
                    2
                )
            }
        }
    },
    true
);
    }
}
