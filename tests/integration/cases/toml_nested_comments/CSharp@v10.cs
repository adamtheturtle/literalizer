using System.Collections.Generic;
using System;
var my_data = new Dictionary<string, object> {
    // About the first dotted key.
    // About the second dotted key.
    ["dotted"] = new Dictionary<string, int> {["first"] = 1, ["second"] = 2},
    ["plain"] = 3,  // About the plain key.
    // Before the first entry.
    // Before the second entry.
    ["entries"] = (new Dictionary<string, string> {["name"] = "one"}, new Dictionary<string, string> {["name"] = "two"}),
    // Inside the table.
    ["table"] = new Dictionary<string, int> {["inner"] = 4}
};
