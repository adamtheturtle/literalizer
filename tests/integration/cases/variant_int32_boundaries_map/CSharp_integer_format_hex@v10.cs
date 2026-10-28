using System.Collections.Generic;
using System;
var my_data = new Dictionary<string, object?> {
    ["below"] = -0x80000001,
    ["minimum"] = -0x80000000,
    ["above"] = -0x7fffffff,
    ["nested"] = ValueTuple.Create(0x0)
};
    _ = my_data;
