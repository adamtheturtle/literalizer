using System;
using System.Collections.Generic;
var SharedValues = (
    1,
    2
);
var my_data = new Dictionary<string, object?> {
    ["a"] = SharedValues
};
my_data = new Dictionary<string, object?> {
    ["a"] = SharedValues
};
    _ = my_data;
