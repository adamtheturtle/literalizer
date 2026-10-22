using System.Collections.Generic;
var my_data = new Dictionary<string, object?> {
    ["a"] = new Dictionary<string, int> {
        /* indented */
        ["x"] = 1
    },
    ["b"] = 2
};
    _ = my_data;
