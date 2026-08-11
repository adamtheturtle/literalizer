using System.Collections.Generic;
var my_data = new SortedDictionary<string, object> {
    ["outer"] = new SortedDictionary<string, object> {["a"] = 1, ["b"] = "x", ["c"] = (object?)null}
};
