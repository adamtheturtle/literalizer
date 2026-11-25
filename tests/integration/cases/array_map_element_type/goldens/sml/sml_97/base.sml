datatype val_t =
    SBool of bool
  | SInt of LargeInt.int
  | SReal of real
  | SStr of string
  | SList of val_t list
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("d", SList [SMap [("a", SList [SMap [("b", SList [SInt 1, SList [SReal 2.5, SList [SStr "x", SList [SBool true]]]])]])]])
]
val _ = my_data
