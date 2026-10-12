using System.Collections.Generic;
using System;
var my_data = new Dictionary<string, object> {
    ["minimum"] = -2147483648,
    ["neighbor"] = -2147483647,
    ["maximum"] = 2147483647,
    ["nested"] = ValueTuple.Create(-2147483648)
};
