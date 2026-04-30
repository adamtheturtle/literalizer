datatype val_t =
    SStr of string
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("$ref", SStr "myVar")
]
val _ = my_data
