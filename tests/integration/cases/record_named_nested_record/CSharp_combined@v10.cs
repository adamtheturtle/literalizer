using System.Collections.Generic;
using System;
var my_data = new Dictionary<string, object> {
    ["project"] = "alpha",
    ["lead_task"] = new Dictionary<string, object> {["id"] = 100, ["description"] = "first task", ["is_done"] = false, ["blocks"] = (102, 103)}
};
my_data = new Dictionary<string, object> {
    ["project"] = "alpha",
    ["lead_task"] = new Dictionary<string, object> {["id"] = 100, ["description"] = "first task", ["is_done"] = false, ["blocks"] = (102, 103)}
};
