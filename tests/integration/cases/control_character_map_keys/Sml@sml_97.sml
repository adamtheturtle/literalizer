datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("", SInt 1),
    ("a\001b", SInt 2)
]
val _ = my_data
