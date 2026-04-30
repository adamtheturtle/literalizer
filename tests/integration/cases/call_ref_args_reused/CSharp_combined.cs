using System.Collections.Generic;
using System;
var my_data = (
    (new Dictionary<string, string> {["$ref"] = "repeated_var"}, 1),
    (new Dictionary<string, string> {["$ref"] = "single_var"}, 0),
    (new Dictionary<string, string> {["$ref"] = "repeated_var"}, 8)
);
my_data = (
    (new Dictionary<string, string> {["$ref"] = "repeated_var"}, 1),
    (new Dictionary<string, string> {["$ref"] = "single_var"}, 0),
    (new Dictionary<string, string> {["$ref"] = "repeated_var"}, 8)
);
