datatype val_t =
    SStr of string
  | SDate of (int * int * int)
  | SDatetime of ((int * int * int) * (int * int * int))
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("date", SDate (99, 5, 27)),
    ("naive", SDatetime ((1, 1, 1), (12, 30, 0))),
    ("recent", SDatetime ((2024, 5, 27), (10, 0, 0)))
]
val _ = my_data
