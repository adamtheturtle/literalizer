using System.Collections.Generic;
using System;
var my_data = (
    (
        new Dictionary<string, string> {["item"] = "existing"},
        "kept"
        // This comment trails the first pair.
    ),
    (new Dictionary<string, string> {["item"] = "next"}, "also kept"),
    // This comment describes the last pair.
    (new Dictionary<string, string> {["item"] = "last"}, "kept too")
);
my_data = (
    (
        new Dictionary<string, string> {["item"] = "existing"},
        "kept"
        // This comment trails the first pair.
    ),
    (new Dictionary<string, string> {["item"] = "next"}, "also kept"),
    // This comment describes the last pair.
    (new Dictionary<string, string> {["item"] = "last"}, "kept too")
);
