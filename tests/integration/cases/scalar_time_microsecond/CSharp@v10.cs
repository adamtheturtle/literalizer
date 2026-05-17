using System;
using System.Collections.Generic;
var my_data = new Dictionary<string, TimeOnly> {
    ["exact_millisecond"] = new TimeOnly(9, 30, 15, 123),
    ["sub_millisecond"] = new TimeOnly(9, 30, 15, 123, 456)
};
