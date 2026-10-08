using System.Collections.Generic;
using System;
var my_data = new Dictionary<string, object> {
    ["a"] = ((1, 2), ValueTuple.Create(3)),
    ["b"] = (ValueTuple.Create(), ValueTuple.Create(1))
};
