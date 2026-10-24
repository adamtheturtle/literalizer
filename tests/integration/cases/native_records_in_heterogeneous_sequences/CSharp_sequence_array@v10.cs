using System.Collections.Generic;
var my_data = new Dictionary<string, object?> {
    ["h"] = new object?[] {1, "a", new object?[] {2, "b"}, new Dictionary<string, bool[]> {["k"] = new bool[] {true}}}
};
    _ = my_data;
