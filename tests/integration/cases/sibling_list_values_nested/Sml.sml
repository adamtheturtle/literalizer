datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SList of val_t list
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("lint", SList [SInt 2, SList []]),
    ("test", SList [SInt 5, SList [SStr "compile"]])
]
val _ = my_data
