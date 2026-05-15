datatype val_t =
    SBool of bool
  | SInt of LargeInt.int
  | SStr of string
  | SList of val_t list
  | SMap of (string * val_t) list
val my_data : val_t = SList [
    SMap [("id", SInt 100), ("description", SStr "first task"), ("is_done", SBool false), ("blocks", SList [SInt 102, SInt 103])],
    SMap [("id", SInt 101), ("description", SStr "second task"), ("is_done", SBool true), ("blocks", SList [SInt 100])]
]
val _ = my_data
