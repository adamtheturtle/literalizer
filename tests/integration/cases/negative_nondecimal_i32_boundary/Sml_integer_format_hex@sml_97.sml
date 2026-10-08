datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("minimum", SInt (~0x80000000)),
    ("below", SInt (~0xb2d05e00))
]
val _ = my_data
