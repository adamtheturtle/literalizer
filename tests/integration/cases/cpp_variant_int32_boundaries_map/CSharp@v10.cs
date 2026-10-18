using System.Collections.Generic;
using System;
var my_data = new Dictionary<string, object?> {
    ["below"] = -2147483649,
    ["minimum"] = -2147483648,
    ["above"] = -2147483647,
    ["nested"] = ValueTuple.Create(0)
};
    _ = my_data;
