datatype val_t =
    SStr of string
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("a", SMap [("b", SMap [("c", SMap [("$ref", SStr "deep")])])])
]
val _ = my_data
