using System.Collections.Generic;
using System;
var my_data = new SortedDictionary<string, object> {
    // About the first dotted key.
    // About the second dotted key.
    ["dotted"] = new SortedDictionary<string, int> {["first"] = 1, ["second"] = 2},
    ["plain"] = 3,  // About the plain key.
    // Before the first entry.
    // Before the second entry.
    ["entries"] = (new SortedDictionary<string, string> {["name"] = "one"}, new SortedDictionary<string, string> {["name"] = "two"}),
    // Inside the table.
    ["table"] = new SortedDictionary<string, int> {["inner"] = 4}
};
    _ = my_data;
