using System.Collections.Generic;
var my_data = new Dictionary<string, string> {
    // heading
    ["a"] = "single ' // data",
    ["b"] = "linecontinuation",
    ["c"] = "\\",  // actual comment
    ["d"] = "\u2028\u2029"  // final comment
};
my_data = new Dictionary<string, string> {
    // heading
    ["a"] = "single ' // data",
    ["b"] = "linecontinuation",
    ["c"] = "\\",  // actual comment
    ["d"] = "\u2028\u2029"  // final comment
};
    _ = my_data;
