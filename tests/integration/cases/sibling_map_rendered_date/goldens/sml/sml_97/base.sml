datatype val_t =
    SStr of string
  | SDate of (int * int * int)
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("a", SMap [("k", SDate (2020, 1, 1))]),
    ("b", SMap [("k", SStr "string")])
]
val _ = my_data
