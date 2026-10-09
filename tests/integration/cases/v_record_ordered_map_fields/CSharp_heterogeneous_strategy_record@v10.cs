using System.Collections.Generic;
record Record0(Dictionary<string, object> Numbers, Dictionary<string, object> Words, Dictionary<string, object> Nested, Dictionary<string, object> Empty, bool Flag, Dictionary<string, object> NestedMaps, Dictionary<string, object> EmptyNestedMaps);
class Check {
    public static void Main() {
var my_data = new Record0(
    new Dictionary<string, object> {
        ["first"] = 1
    },
    new Dictionary<string, object> {
        ["first"] = "s"
    },
    new Dictionary<string, object> {
        ["first"] = new int[] {
            1,
            2
        }
    },
    new Dictionary<string, object> {},
    true,
    new Dictionary<string, object> {
        ["first"] = new Dictionary<string, object> {
            ["nested"] = 1
        }
    },
    new Dictionary<string, object> {
        ["first"] = new Dictionary<string, object> {}
    }
);
    }
}
