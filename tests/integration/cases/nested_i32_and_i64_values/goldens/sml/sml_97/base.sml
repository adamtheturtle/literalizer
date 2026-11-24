datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SList of val_t list
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("values", SList [SInt 1, SInt 2147483648])
]
val _ = my_data
