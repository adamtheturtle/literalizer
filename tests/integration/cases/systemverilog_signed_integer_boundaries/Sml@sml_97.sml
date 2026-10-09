datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("i32_below", SInt (~2147483649)),
    ("i32_minimum", SInt (~2147483648)),
    ("i32_above", SInt (~2147483647)),
    ("i32_maximum", SInt 2147483647),
    ("i32_over", SInt 2147483648),
    ("i64_minimum", SInt (~9223372036854775808)),
    ("i64_maximum", SInt 9223372036854775807)
]
val _ = my_data
