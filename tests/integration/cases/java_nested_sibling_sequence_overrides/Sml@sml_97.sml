datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SList of val_t list
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("a", SList [SList [SInt 1], SList [SInt 2]]),
    ("b", SList [SList [SStr "x"], SList [SStr "y"]])
]
val _ = my_data
