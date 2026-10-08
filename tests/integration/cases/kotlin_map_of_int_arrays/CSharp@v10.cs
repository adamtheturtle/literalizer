using System.Collections.Generic;
using System;
var my_data = new Dictionary<string, object> {
    ["a"] = ValueTuple.Create((1, 2)),
    ["b"] = ValueTuple.Create(ValueTuple.Create(3))
};
