datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SList of val_t list
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("minimum", SInt (~2147483648)),
    ("neighbor", SInt (~2147483647)),
    ("maximum", SInt 2147483647),
    ("nested", SList [SInt (~2147483648)])
]
val _ = my_data
