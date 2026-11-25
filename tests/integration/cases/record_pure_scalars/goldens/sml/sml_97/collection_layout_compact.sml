datatype val_t =
    SBool of bool
  | SInt of LargeInt.int
  | SReal of real
  | SStr of string
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("name", SStr "Alice"),
    ("age", SInt 30),
    ("active", SBool true),
    ("score", SReal 4.5)
]
val _ = my_data
