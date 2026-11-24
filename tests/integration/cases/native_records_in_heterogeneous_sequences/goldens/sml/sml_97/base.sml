datatype val_t =
    SBool of bool
  | SInt of LargeInt.int
  | SStr of string
  | SList of val_t list
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("h", SList [SInt 1, SStr "a", SList [SInt 2, SStr "b"], SMap [("k", SList [SBool true])]])
]
val _ = my_data
