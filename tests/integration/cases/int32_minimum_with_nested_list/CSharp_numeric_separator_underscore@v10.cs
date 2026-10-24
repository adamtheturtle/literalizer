using System.Collections.Generic;
using System;
var my_data = new Dictionary<string, object?> {
    ["minimum"] = -2_147_483_648,
    ["neighbor"] = -2_147_483_647,
    ["maximum"] = 2_147_483_647,
    ["nested"] = ValueTuple.Create(-2_147_483_648)
};
    _ = my_data;
