datatype val_t =
    SStr of string
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("morning", "09:30:00"),
    ("afternoon", "14:15:00"),
    ("evening", "23:59:59")
]
val _ = my_data
