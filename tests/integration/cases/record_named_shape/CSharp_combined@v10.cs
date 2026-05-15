using System.Collections.Generic;
using System;
var my_data = (
    new Dictionary<string, object> {["id"] = 100, ["description"] = "first task", ["is_done"] = false, ["blocks"] = (102, 103)},
    new Dictionary<string, object> {["id"] = 101, ["description"] = "second task", ["is_done"] = true, ["blocks"] = (100)}
);
my_data = (
    new Dictionary<string, object> {["id"] = 100, ["description"] = "first task", ["is_done"] = false, ["blocks"] = (102, 103)},
    new Dictionary<string, object> {["id"] = 101, ["description"] = "second task", ["is_done"] = true, ["blocks"] = (100)}
);
