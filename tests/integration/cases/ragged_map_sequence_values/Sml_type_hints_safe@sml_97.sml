datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SList of val_t list
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("a", SList [SMap [("item", SList [SInt 1])]]),
    ("b", SList [SMap [("item", SList [SInt 2, SInt 3])]])
]
val _ = my_data
