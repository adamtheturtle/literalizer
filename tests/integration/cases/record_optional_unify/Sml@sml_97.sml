datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SList of val_t list
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("items", SList [SMap [("id", SInt 1)], SMap [("id", SInt 2), ("count", SInt 10)], SMap [("id", SInt 3), ("count", SInt 20)]])
]
val _ = my_data
