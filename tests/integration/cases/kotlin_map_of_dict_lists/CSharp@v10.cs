using System.Collections.Generic;
using System;
var my_data = new Dictionary<string, object> {
    ["a"] = ValueTuple.Create(new Dictionary<string, int> {["k"] = 1}),
    ["b"] = ValueTuple.Create(new Dictionary<string, int> {["k"] = 2})
};
