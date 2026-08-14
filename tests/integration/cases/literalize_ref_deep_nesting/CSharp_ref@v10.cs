using System;
using System.Collections.Generic;
var Deep = (
    (
        "one",
        "two"
    ),
    (
        "three",
        "four"
    )
);
var my_data = new Dictionary<string, object> {
    ["a"] = new Dictionary<string, object> {
        ["b"] = new Dictionary<string, object> {
            ["c"] = Deep
        }
    }
};
