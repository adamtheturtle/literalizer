datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SMap of (string * val_t) list
val other : val_t = SStr "true"
val my_data : val_t = SMap [
    ("main", SMap [("x", SInt 1), ("y", SStr "s")])
]
val _ = my_data
