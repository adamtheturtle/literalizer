datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SList of val_t list
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("below", SInt (~2147483649)),
    ("minimum", SInt (~2147483648)),
    ("above", SInt (~2147483647)),
    ("nested", SList [SInt 0])
]
val _ = my_data
