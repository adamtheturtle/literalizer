using System.Collections.Generic;
var my_data = new Dictionary<string, object> {
    ["outer"] = new Dictionary<string, object> {["a"] = 1, ["b"] = "x", ["c"] = (object?)null}
};
my_data = new Dictionary<string, object> {
    ["outer"] = new Dictionary<string, object> {["a"] = 1, ["b"] = "x", ["c"] = (object?)null}
};
