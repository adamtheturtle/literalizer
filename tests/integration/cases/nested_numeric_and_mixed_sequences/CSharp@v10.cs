using System.Collections.Generic;
using System;
var my_data = new Dictionary<string, object?> {
    ["numbers"] = (1, 2),
    ["nested"] = new Dictionary<string, object?> {["inner"] = ValueTuple.Create(3)},
    ["mixed"] = (4, "five")
};
    _ = my_data;
