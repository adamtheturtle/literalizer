datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SList of val_t list
  | SMap of (string * val_t) list
val x : val_t = SMap [
    ("_", SStr "_")
]
val my_data : val_t = SList [
    x,
    SInt 1,
    SInt 2
]
val _ = my_data
