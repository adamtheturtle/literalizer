datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("a", SInt 1),
    ("b", SInt 3000000000),
    ("c", SStr "x")
]
val _ = my_data
