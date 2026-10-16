datatype val_t =
    SStr of string
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("text", SStr "a\"//b")
]
val _ = my_data
