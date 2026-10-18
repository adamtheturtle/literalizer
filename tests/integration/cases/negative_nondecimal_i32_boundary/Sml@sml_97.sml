datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("minimum", SInt (~2147483648)),
    ("below", SInt (~3000000000))
]
val _ = my_data
