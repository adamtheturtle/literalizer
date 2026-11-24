datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SList of val_t list
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("a", SList [SMap [("k", SInt 1)]]),
    ("b", SList [SMap [("k", SInt 2)]])
]
val _ = my_data
