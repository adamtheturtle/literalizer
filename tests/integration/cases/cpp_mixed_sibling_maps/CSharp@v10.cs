using System.Collections.Generic;
using System;
var my_data = (
    (new Dictionary<string, object> {["a"] = 1}, new Dictionary<string, object> {["a"] = (object?)null}, 42),
    (new Dictionary<string, object> {["a"] = 1}, new Dictionary<string, object> {["a"] = "s"}, 42),
    (new Dictionary<string, object> {["a"] = 1}, new Dictionary<string, object> {["a"] = (object?)null}),
    (new Dictionary<string, object> {["a"] = 1}, new Dictionary<string, object> {["a"] = "s"})
);
