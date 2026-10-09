using System.Collections.Generic;
record Record0(Dictionary<string, object> Values, bool Flag, Dictionary<string, object> NestedValues, Dictionary<string, object> ListValues);
class Check {
    public static void Main() {
var my_data = new Record0(
    new Dictionary<string, object> {
        ["first"] = 2208988800
    },
    true,
    new Dictionary<string, object> {
        ["first"] = new Dictionary<string, object> {
            ["nested"] = 2208988800
        }
    },
    new Dictionary<string, object> {
        ["first"] = new int[] {
            2208988800
        }
    }
);
    }
}
