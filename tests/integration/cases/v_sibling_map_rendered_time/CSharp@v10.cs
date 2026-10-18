using System;
using System.Collections.Generic;
var my_data = new Dictionary<string, object?> {
    ["a"] = new Dictionary<string, object?> {["k"] = new TimeOnly(7, 30, 0)},
    ["b"] = new Dictionary<string, object?> {["k"] = "string"}
};
    _ = my_data;
