using System.Collections.Generic;
using System;
var my_data = (
    new Dictionary<string, object?> {["input"] = new Dictionary<string, object?> {["name"] = "alice", ["city"] = "paris"}, ["expected"] = new Dictionary<string, object?> {["count"] = 1, ["total"] = 2}},
    new Dictionary<string, object?> {["input"] = new Dictionary<string, object?> {["name"] = 10, ["city"] = 20}, ["expected"] = new Dictionary<string, object?> {["count"] = "done", ["total"] = "pending"}}
);
    _ = my_data;
