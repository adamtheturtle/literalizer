using System.Collections.Generic;
using System;
var my_data = new Dictionary<string, object?> {
    ["outer"] = ValueTuple.Create(new Dictionary<string, int> {["_"] = 1})
};
    _ = my_data;
