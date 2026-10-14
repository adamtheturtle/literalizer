using System.Collections.Generic;
using System;
var my_data = new Dictionary<string, object?> {
    ["below"] = -0b10000000000000000000000000000001,
    ["minimum"] = -0b10000000000000000000000000000000,
    ["above"] = -0b1111111111111111111111111111111,
    ["nested"] = ValueTuple.Create(0b0)
};
    _ = my_data;
