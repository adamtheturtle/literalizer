datatype val_t =
    SStr of string
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("v", SStr "a\239\187\191b")
]
val _ = my_data
