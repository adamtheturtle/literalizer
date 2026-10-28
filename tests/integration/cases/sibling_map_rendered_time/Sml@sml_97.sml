datatype val_t =
    SStr of string
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("a", SMap [("k", SStr "07:30:00")]),
    ("b", SMap [("k", SStr "string")])
]
val _ = my_data
