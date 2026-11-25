datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("a_b", SInt 0x1),
    ("a-b", SInt 0x2),
    ("averyveryverylongkeynamethatgoesonandonandon", SInt 0x3),
    ("averyveryverylongkeynamethatgoesonandmore", SInt 0x4)
]
val _ = my_data
