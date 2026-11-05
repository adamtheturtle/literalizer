datatype val_t =
    SBool of bool
  | SStr of string
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("keep", SBool true),
    ("skip", SBool false)
]
val _ = my_data
