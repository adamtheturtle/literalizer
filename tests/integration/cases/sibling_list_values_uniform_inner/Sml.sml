datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SList of val_t list
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("lint", SList [SInt 2, SList [SInt 1]]),
    ("test", SList [SInt 5, SList [SInt 7]])
]
val _ = my_data
