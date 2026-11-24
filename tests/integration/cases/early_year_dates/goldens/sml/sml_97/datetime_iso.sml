datatype val_t =
    SStr of string
  | SDate of (int * int * int)
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("date", SDate (99, 5, 27)),
    ("naive", SStr "0001-01-01T12:30:00"),
    ("recent", SStr "2024-05-27T10:00:00")
]
val _ = my_data
