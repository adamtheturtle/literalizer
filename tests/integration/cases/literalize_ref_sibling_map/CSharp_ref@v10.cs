using System.Collections.Generic;
using System;
var SiblingMap = new Dictionary<string, int> {
    ["k"] = 2
};
var my_data = (
    new Dictionary<string, int> {["k"] = 1},
    SiblingMap
);
