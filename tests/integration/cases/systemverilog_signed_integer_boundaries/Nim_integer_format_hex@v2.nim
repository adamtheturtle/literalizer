import json
var my_data = %* {
    "i32_below": -0x80000001'i64,
    "i32_minimum": -0x80000000'i64,
    "i32_above": -0x7fffffff'i64,
    "i32_maximum": 0x7fffffff'i64,
    "i32_over": 0x80000000'i64,
    "i64_minimum": cast[int64](0x8000000000000000'u64),
    "i64_maximum": 0x7fffffffffffffff'i64
}
