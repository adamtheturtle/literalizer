using System.Collections.Generic;
using System;
var my_data = new Dictionary<string, object?> {
    ["minimum"] = -0b10000000000000000000000000000000,
    ["neighbor"] = -0b1111111111111111111111111111111,
    ["maximum"] = 0b1111111111111111111111111111111,
    ["nested"] = ValueTuple.Create(-0b10000000000000000000000000000000)
};
    _ = my_data;
