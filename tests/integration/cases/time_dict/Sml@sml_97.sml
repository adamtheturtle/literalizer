datatype val_t =
    SStr of string
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("morning", SStr "09:30:00"),
    ("afternoon", SStr "14:15:00"),
    ("evening", SStr "23:59:59")
]
val _ = my_data
