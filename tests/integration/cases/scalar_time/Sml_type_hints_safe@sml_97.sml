datatype val_t =
    SStr of string
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("starts_at", SStr "09:30:00")
]
val _ = my_data
