using System.Collections.Generic;
using System;
var my_data = (
    ValueTuple.Create(new Dictionary<string, int> {["value"] = 1}),
    ValueTuple.Create(new Dictionary<string, long> {["value"] = 1099511627776})
);
    _ = my_data;
