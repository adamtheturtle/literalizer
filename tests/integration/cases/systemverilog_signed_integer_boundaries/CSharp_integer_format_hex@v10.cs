using System.Collections.Generic;
var my_data = new Dictionary<string, long> {
    ["i32_below"] = -0x80000001,
    ["i32_minimum"] = -0x80000000,
    ["i32_above"] = -0x7fffffff,
    ["i32_maximum"] = 0x7fffffff,
    ["i32_over"] = 0x80000000,
    ["i64_minimum"] = -0x8000000000000000,
    ["i64_maximum"] = 0x7fffffffffffffff
};
