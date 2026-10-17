datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("quote\"backslash\\", SInt 1),
    ("line\nbreak", SInt 2),
    ("$(literal)${text}", SInt 3),
    ("RStr prefix", SInt 4)
]
val _ = my_data
