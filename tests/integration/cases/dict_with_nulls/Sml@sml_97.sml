datatype val_t =
    SNull
  | SInt of LargeInt.int
  | SStr of string
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("name", SStr "Alice"),
    ("score", SNull),
    ("age", SInt 30)
]
val _ = my_data
