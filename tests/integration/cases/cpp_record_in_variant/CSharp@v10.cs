using System.Collections.Generic;
using System;
var my_data = new Dictionary<string, object> {
    ["h"] = (1, "a", (2, "b"), new Dictionary<string, object> {["k"] = ValueTuple.Create(true)})
};
