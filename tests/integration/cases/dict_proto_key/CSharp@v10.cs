using System.Collections.Generic;
var my_data = new Dictionary<string, object> {
    ["__proto__"] = new Dictionary<string, int> {["x"] = 1},
    ["n"] = new Dictionary<string, int> {["__proto__"] = 3},
    ["y"] = 2
};
