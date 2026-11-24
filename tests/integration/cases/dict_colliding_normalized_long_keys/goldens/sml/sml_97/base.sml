datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("a_b", SInt 1),
    ("a-b", SInt 2),
    ("averyveryverylongkeynamethatgoesonandonandon", SInt 3),
    ("averyveryverylongkeynamethatgoesonandmore", SInt 4)
]
val _ = my_data
