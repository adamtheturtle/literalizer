datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SList of val_t list
  | SMap of (string * val_t) list
val shared : val_t = SList [
    SList [SInt 1, SInt 2],
    SMap [("value", SInt 1)]
]
val my_data : val_t = SList [
    shared,
    shared
]
val _ = my_data
