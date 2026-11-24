using System.Collections.Generic;
var my_data = new SortedDictionary<string, object> {
    // first dotted key
    // second dotted key
    ["a"] = new SortedDictionary<string, int> {["b"] = 1, ["c"] = 2}
};
    _ = my_data;
