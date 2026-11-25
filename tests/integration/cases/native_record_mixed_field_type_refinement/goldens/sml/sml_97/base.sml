datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SList of val_t list
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("first", SMap [("items", SList [SInt 1, SMap [("value", SInt 2)]])]),
    ("second", SMap [("items", SList [SInt 1, SMap [("value", SStr "s")]])])
]
val _ = my_data
