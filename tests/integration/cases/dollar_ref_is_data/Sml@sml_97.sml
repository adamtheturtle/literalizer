datatype val_t =
    SStr of string
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("value", SMap [("$ref", SStr "foo")])
]
val _ = my_data
