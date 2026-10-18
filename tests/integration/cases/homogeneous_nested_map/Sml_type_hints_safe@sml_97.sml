datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("first", SMap [("x", SInt 1), ("y", SInt 2)]),
    ("second", SMap [("z", SInt 3)])
]
val _ = my_data
