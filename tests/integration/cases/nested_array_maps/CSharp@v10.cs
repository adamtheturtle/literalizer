using System.Collections.Generic;
using System;
var my_data = new Dictionary<string, object> {
    ["groups"] = (ValueTuple.Create(new Dictionary<string, int> {["id"] = 1}), ValueTuple.Create(new Dictionary<string, int> {["id"] = 2}))
};
