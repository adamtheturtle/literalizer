using System.Collections.Generic;
using System;
var my_data = new Dictionary<string, object> {
    ["a"] = (new Dictionary<string, int> {}, new Dictionary<string, int> {["x"] = 1}),
    ["b"] = (ValueTuple.Create(), ValueTuple.Create(1))
};
