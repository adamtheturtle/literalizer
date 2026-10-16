datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("lower", SInt 3735928559),
    ("upper", SInt 31),
    ("negative", SInt (~16)),
    ("zero", SInt 0)
]
val _ = my_data
