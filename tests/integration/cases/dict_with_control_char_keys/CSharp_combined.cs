using System.Collections.Generic;
var my_data = new Dictionary<string, string> {
    ["key\nwith\nnewlines"] = "value1",
    ["key\twith\ttabs"] = "value2",
    [""] = "value3"
};
my_data = new Dictionary<string, string> {
    ["key\nwith\nnewlines"] = "value1",
    ["key\twith\ttabs"] = "value2",
    [""] = "value3"
};
