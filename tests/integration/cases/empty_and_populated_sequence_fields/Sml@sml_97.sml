datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SList of val_t list
  | SMap of (string * val_t) list
val my_data : val_t = SList [
    SMap [("value", SList [])],
    SMap [("value", SList [SInt 1])]
]
val _ = my_data
