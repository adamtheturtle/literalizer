datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("text", SStr "Record0("),
    ("number", SInt 0x1)
]
val _ = my_data
