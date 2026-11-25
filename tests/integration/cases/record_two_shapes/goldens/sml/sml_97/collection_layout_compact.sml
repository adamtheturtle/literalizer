datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("metrics", SMap [("count", SInt 100), ("rate", SInt 50)]),
    ("flags", SMap [("retries", SInt 3), ("timeout", SInt 30)])
]
val _ = my_data
