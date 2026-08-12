using System.Collections.Generic;
using System;
var my_data = new Dictionary<string, object> {
    ["a"] = new Dictionary<string, int> {
        // inner note
        ["b"] = 1  // inline b
    },
    ["list"] = (
        1,  // first
        2  // second
    )
};
