datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("id", SInt 1),
    ("owner", SMap [("name", SStr "Alice"), ("age", SInt 30)])
]
val _ = my_data
