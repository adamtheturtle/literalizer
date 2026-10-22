using System.Collections.Generic;
using System;
var my_data = new Dictionary<string, object?> {
    ["a"] = ValueTuple.Create(new Dictionary<string, object?> {["item"] = ValueTuple.Create(1)}),
    ["b"] = ValueTuple.Create(new Dictionary<string, object?> {["item"] = (2, 3)})
};
    _ = my_data;
