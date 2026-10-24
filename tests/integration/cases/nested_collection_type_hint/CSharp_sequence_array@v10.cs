using System.Collections.Generic;
var my_data = new Dictionary<string, object?> {
    ["a"] = new Dictionary<string, int>[] {new Dictionary<string, int> {["b"] = 1}}
};
    _ = my_data;
