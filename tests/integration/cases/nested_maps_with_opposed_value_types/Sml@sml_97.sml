datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SList of val_t list
  | SMap of (string * val_t) list
val my_data : val_t = SList [
    SMap [("input", SMap [("name", SStr "alice"), ("city", SStr "paris")]), ("expected", SMap [("count", SInt 1), ("total", SInt 2)])],
    SMap [("input", SMap [("name", SInt 10), ("city", SInt 20)]), ("expected", SMap [("count", SStr "done"), ("total", SStr "pending")])]
]
val _ = my_data
