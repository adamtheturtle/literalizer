using System.Collections.Generic;
var my_data = new Dictionary<string, int> {
    ["quote\"backslash\\"] = 1,
    ["line\nbreak"] = 2,
    ["$(literal)${text}"] = 3,
    ["RStr prefix"] = 4
};
    _ = my_data;
