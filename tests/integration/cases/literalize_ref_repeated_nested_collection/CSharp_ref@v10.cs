using System.Collections.Generic;
using System;
var Shared = (
    (1, 2),
    new Dictionary<string, int> {["value"] = 1}
);
var my_data = (
    Shared,
    Shared
);
    _ = my_data;
