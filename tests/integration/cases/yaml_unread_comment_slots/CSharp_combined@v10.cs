using System.Collections.Generic;
using System;
var my_data = new Dictionary<string, object> {
    ["flow"] = (
        1,
        // After the first element.
        2
    ),
    // Between the key and its value.
    ["gap"] = 3,
    // On the block scalar header.
    ["block"] = "Text.\n",
    ["nested"] = (
        1,
        1
        // On the nested alias.
    ),
    ["anchored"] = 4,
    ["alias"] = 4
    // On the alias.
};
my_data = new Dictionary<string, object> {
    ["flow"] = (
        1,
        // After the first element.
        2
    ),
    // Between the key and its value.
    ["gap"] = 3,
    // On the block scalar header.
    ["block"] = "Text.\n",
    ["nested"] = (
        1,
        1
        // On the nested alias.
    ),
    ["anchored"] = 4,
    ["alias"] = 4
    // On the alias.
};
