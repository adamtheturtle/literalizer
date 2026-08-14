datatype val_t =
    SStr of string
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("explicit_string", SStr "5"),
    ("six", SStr "explicitly tagged key")
]
val _ = my_data
