using System.Collections.Generic;
using System;
var my_data = (
    new Dictionary<string, object> {["outer"] = new Dictionary<string, object> {["inner"] = new Dictionary<string, int> {["x"] = 1}}},
    new Dictionary<string, object> {["outer"] = new Dictionary<string, object> {["inner"] = new Dictionary<string, object> {}}}
);
