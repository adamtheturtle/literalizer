using System;
using System.Collections.Generic;
var my_data = new Dictionary<string, object> {
    ["name"] = "Alice",
    ["age"] = 30,
    ["active"] = true,
    ["score"] = (object?)null,
    ["joined"] = new DateOnly(2024, 1, 15),
    ["last_login"] = new DateTime(2024, 1, 15, 12, 30, 0),
    ["avatar"] = "48656c6c6f"
};
