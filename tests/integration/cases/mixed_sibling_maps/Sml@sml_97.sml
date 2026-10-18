datatype val_t =
    SNull
  | SInt of LargeInt.int
  | SStr of string
  | SList of val_t list
  | SMap of (string * val_t) list
val my_data : val_t = SList [
    SList [SMap [("a", SInt 1)], SMap [("a", SNull)], SInt 42],
    SList [SMap [("a", SInt 1)], SMap [("a", SStr "s")], SInt 42],
    SList [SMap [("a", SInt 1)], SMap [("a", SNull)]],
    SList [SMap [("a", SInt 1)], SMap [("a", SStr "s")]]
]
val _ = my_data
