datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SList of val_t list
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("rows", SList [SMap [("x", SInt 1), ("y", SStr "a")], SMap [("x", SInt 2), ("y", SStr "b")]])
]
val _ = my_data
