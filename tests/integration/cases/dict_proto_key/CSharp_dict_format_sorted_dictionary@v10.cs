using System.Collections.Generic;
var my_data = new SortedDictionary<string, object?> {
    ["__proto__"] = new SortedDictionary<string, int> {["x"] = 1},
    ["n"] = new SortedDictionary<string, int> {["__proto__"] = 3},
    ["y"] = 2
};
    _ = my_data;
