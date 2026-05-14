datatype val_t =
    SStr of string
  | SMap of (string * val_t) list
val deep : val_t = SMap [
    ("_", SStr "_")
]
val my_data : val_t = SMap [
    ("a", SMap [("b", SMap [("c", deep)])])
]
val _ = my_data
