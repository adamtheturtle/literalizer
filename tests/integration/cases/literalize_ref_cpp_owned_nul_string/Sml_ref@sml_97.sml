datatype val_t =
    SStr of string
  | SMap of (string * val_t) list
val shared : val_t = SStr "a\000b"
val my_data : val_t = SMap [
    ("value", shared)
]
val _ = my_data
