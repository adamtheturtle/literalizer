using System;
using System.Collections.Generic;
var Shared = (
    1,
    2
);
var my_data = ValueTuple.Create(
    new Dictionary<string, object?> {["left"] = Shared, ["right"] = Shared}
);
    _ = my_data;
