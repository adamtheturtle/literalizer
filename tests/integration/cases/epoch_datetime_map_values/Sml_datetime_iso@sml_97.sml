datatype val_t =
    SStr of string
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("within_i32", SStr "2024-01-15T12:00:00"),
    ("beyond_i32", SStr "2099-06-15T08:30:00")
]
val _ = my_data
