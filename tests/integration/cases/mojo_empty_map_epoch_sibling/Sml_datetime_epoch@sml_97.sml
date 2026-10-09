datatype val_t =
    SStr of string
  | SInt of LargeInt.int
  | SList of val_t list
  | SMap of (string * val_t) list
val my_data : val_t = SList [
    SMap [("timestamp", SInt 1577836800)],
    SMap []
]
val _ = my_data
