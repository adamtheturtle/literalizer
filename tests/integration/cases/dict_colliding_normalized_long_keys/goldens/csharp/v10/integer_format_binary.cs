using System.Collections.Generic;
var my_data = new Dictionary<string, int> {
    ["a_b"] = 0b1,
    ["a-b"] = 0b10,
    ["averyveryverylongkeynamethatgoesonandonandon"] = 0b11,
    ["averyveryverylongkeynamethatgoesonandmore"] = 0b100
};
    _ = my_data;
