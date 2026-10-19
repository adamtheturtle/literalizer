using System.Collections.Generic;
using System;
var my_data = new Dictionary<string, object?> {
    ["first"] = ((1, "value"), ValueTuple.Create()),
    ["second"] = (ValueTuple.Create(), (2, "other"))
};
    _ = my_data;
