using System.Collections.Generic;
using System;
var my_data = new Dictionary<string, object?> {
    ["a"] = ValueTuple.Create(),
    ["b"] = new HashSet<int> {1, 2}
};
    _ = my_data;
