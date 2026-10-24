using System.Collections.Generic;
using System;
var my_data = new Dictionary<string, object?> {
    ["filled"] = (1, "value"),
    ["empty"] = ValueTuple.Create()
};
    _ = my_data;
