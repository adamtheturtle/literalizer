using System.Collections.Generic;
var x = new Dictionary<string, object> {
    ["key\nwith\nnewlines"] = "value1",
    ["key\twith\ttabs"] = "value2",
    [""] = "value3"
};
