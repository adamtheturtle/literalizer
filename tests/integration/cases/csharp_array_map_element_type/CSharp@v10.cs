using System.Collections.Generic;
using System;
var my_data = new Dictionary<string, object> {
    ["d"] = ValueTuple.Create(new Dictionary<string, object> {["a"] = ValueTuple.Create(new Dictionary<string, object> {["b"] = (1, (2.5, ("x", ValueTuple.Create(true))))})})
};
