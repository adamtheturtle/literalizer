using System.Collections.Generic;
record Record1(int[] Numbers, string[] Strings);
record Record0(Dictionary<string, object> OmapValue, Record1 SiblingLists, string[] RefMarkerPresent);
class Check {
    public static void Main() {
var my_data = new Record0(
    new Dictionary<string, object> {
        ["first"] = 1
    },
    new Record1(
        new int[] {
            1,
            2
        },
        new string[] {
            "x",
            "y"
        }
    ),
    new string[] {
        "$keep",
        "z"
    }
);
    }
}
