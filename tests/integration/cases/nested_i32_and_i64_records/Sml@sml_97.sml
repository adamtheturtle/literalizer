datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SList of val_t list
  | SMap of (string * val_t) list
val my_data : val_t = SList [
    SList [SMap [("value", SInt 1)]],
    SList [SMap [("value", SInt 1099511627776)]]
]
val _ = my_data
