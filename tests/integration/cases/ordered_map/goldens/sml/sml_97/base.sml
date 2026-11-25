datatype val_t =
    SBool of bool
  | SInt of LargeInt.int
  | SStr of string
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("name", SStr "Alice"),
    ("age", SInt 30),
    ("active", SBool true)
]
val _ = my_data
