import json
var my_data = %* {
    "i32_below": -0o20000000001'i64,
    "i32_minimum": -0o20000000000'i64,
    "i32_above": -0o17777777777'i64,
    "i32_maximum": 0o17777777777'i64,
    "i32_over": 0o20000000000'i64,
    "i64_minimum": cast[int64](0o1000000000000000000000'u64),
    "i64_maximum": 0o777777777777777777777'i64
}
