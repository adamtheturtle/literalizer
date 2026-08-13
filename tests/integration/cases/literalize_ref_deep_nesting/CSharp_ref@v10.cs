using System;
using System.Collections.Generic;
var Deep = (
    (
        1,
        2
    ),
    (
        3,
        4
    )
);
var my_data = new Dictionary<string, object> {
    ["a"] = new Dictionary<string, object> {
        ["b"] = new Dictionary<string, object> {
            ["c"] = Deep
        }
    }
};
