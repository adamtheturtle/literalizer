datatype val_t =
    SBool of bool
  | SInt of LargeInt.int
  | SStr of string
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("keep", SBool true),
    ("skip", SInt 0)
]
val _ = my_data
