using System.Collections.Generic;
using System;
var my_data = new Dictionary<string, object> {
    ["a"] = new Dictionary<string, object> {
        ["b"] = ValueTuple.Create(1),
        // Outdented from the sequence, so the inner mapping claims this.
        ["c"] = 2
    },
    // Outdented from the inner mapping too, so the root claims this.
    ["d"] = 3
};
my_data = new Dictionary<string, object> {
    ["a"] = new Dictionary<string, object> {
        ["b"] = ValueTuple.Create(1),
        // Outdented from the sequence, so the inner mapping claims this.
        ["c"] = 2
    },
    // Outdented from the inner mapping too, so the root claims this.
    ["d"] = 3
};
