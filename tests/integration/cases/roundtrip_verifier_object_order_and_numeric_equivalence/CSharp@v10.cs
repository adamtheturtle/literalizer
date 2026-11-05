using System.Collections.Generic;
using System;
var my_data = new Dictionary<string, object?> {
    ["b"] = (object?)null,
    ["a"] = new Dictionary<string, object> {["y"] = ValueTuple.Create(1.0), ["x"] = false}
};
    _ = my_data;
