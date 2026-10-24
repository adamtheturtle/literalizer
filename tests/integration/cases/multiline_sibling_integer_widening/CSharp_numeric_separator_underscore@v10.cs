using System.Collections.Generic;
using System;
var my_data = new Dictionary<string, object?> {
    ["a"] = ValueTuple.Create(1),
    ["b"] = ValueTuple.Create(1_099_511_627_776)
};
    _ = my_data;
