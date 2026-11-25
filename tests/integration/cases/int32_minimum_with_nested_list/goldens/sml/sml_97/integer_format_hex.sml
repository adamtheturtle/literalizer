datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SList of val_t list
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("minimum", SInt (~0x80000000)),
    ("neighbor", SInt (~0x7fffffff)),
    ("maximum", SInt 0x7fffffff),
    ("nested", SList [SInt (~0x80000000)])
]
val _ = my_data
