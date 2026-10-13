#nullable enable annotations
using System.Collections.Generic;
using System;
var my_data = (
    new SortedDictionary<string, object> {["scores"] = (1, 2)},
    new SortedDictionary<string, object> {["scores"] = (3, 4)}
);
    _ = my_data;
