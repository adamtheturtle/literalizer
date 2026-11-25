datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("a", SInt 0x1),
    ("b", SInt 0x10000000000)
]
val _ = my_data
