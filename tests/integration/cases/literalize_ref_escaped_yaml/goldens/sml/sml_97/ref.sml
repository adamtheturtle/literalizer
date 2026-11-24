datatype val_t =
    SStr of string
  | SMap of (string * val_t) list
val existing : val_t = SMap [
    ("_", SStr "_")
]
val my_data : val_t = existing
val _ = my_data
