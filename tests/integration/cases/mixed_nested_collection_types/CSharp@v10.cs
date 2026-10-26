using System.Collections.Generic;
using System;
var my_data = new Dictionary<string, object?> {
    ["lists"] = (ValueTuple.Create(1), ValueTuple.Create("x"), ValueTuple.Create()),
    ["maps"] = (new Dictionary<string, object?> {["x"] = 1}, new Dictionary<string, object?> {["x"] = "s"}),
    ["empties"] = new Dictionary<string, object?> {["a"] = ValueTuple.Create(1), ["b"] = ValueTuple.Create()}
};
    _ = my_data;
