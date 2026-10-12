using System.Collections.Generic;
using System;
var my_data = new Dictionary<string, object> {
    ["minimum"] = -0x80000000,
    ["neighbor"] = -0x7fffffff,
    ["maximum"] = 0x7fffffff,
    ["nested"] = ValueTuple.Create(-0x80000000)
};
