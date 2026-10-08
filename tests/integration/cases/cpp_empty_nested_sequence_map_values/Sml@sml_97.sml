datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SList of val_t list
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("alpha", SList [SInt 2, SList []]),
    ("beta", SList [SInt 5, SList [SStr "x"]])
]
val _ = my_data
