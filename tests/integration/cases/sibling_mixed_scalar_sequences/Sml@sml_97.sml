datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SList of val_t list
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("left", SList [SInt 1, SStr "one"]),
    ("right", SList [SInt 2, SStr "two"])
]
val _ = my_data
