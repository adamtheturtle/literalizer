datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("i32_below", SInt (~0x80000001)),
    ("i32_minimum", SInt (~0x80000000)),
    ("i32_above", SInt (~0x7fffffff)),
    ("i32_maximum", SInt 0x7fffffff),
    ("i32_over", SInt 0x80000000),
    ("i64_minimum", SInt (~0x8000000000000000)),
    ("i64_maximum", SInt 0x7fffffffffffffff)
]
val _ = my_data
