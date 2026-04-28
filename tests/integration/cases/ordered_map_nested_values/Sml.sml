datatype val_t =
    SStr of string
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("name", SStr "Alice"),
    ("scores", SMap [("1", SStr "first"), ("2", SStr "second")])
]
val _ = my_data
