datatype val_t =
    SStr of string
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("0a", SStr "first"),
    ("1b", SStr "second")
]
val _ = my_data
