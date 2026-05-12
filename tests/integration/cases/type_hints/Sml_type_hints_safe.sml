datatype val_t =
    SNull
  | SBool of bool
  | SInt of LargeInt.int
  | SStr of string
  | SDate of (int * int * int)
  | SDatetime of ((int * int * int) * (int * int * int))
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("name", SStr "Alice"),
    ("age", SInt 30),
    ("active", SBool true),
    ("score", SNull),
    ("joined", SDate (2024, 1, 15)),
    ("last_login", SDatetime ((2024, 1, 15), (12, 30, 0))),
    ("avatar", SStr "48656c6c6f")
]
val _ = my_data
