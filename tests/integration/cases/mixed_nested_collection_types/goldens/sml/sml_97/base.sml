datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SList of val_t list
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("lists", SList [SList [SInt 1], SList [SStr "x"], SList []]),
    ("maps", SList [SMap [("x", SInt 1)], SMap [("x", SStr "s")]]),
    ("empties", SMap [("a", SList [SInt 1]), ("b", SList [])])
]
val _ = my_data
