using System.Collections.Generic;
using System;
var my_data = new Dictionary<string, object?> {
    ["x"] = (1, (2, ValueTuple.Create(3)))
};
    _ = my_data;
