datatype val_t =
    SStr of string
  | SInt of LargeInt.int
  | SList of val_t list
  | SMap of (string * val_t) list
val my_data : val_t = SList [
    SMap [("nested", SMap [("times", SList [SInt (~2208988800)])])],
    SMap []
]
val _ = my_data
