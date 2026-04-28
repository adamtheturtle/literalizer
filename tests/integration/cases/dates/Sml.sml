datatype val_t =
    SStr of string
  | SDate of (int * int * int)
  | SDatetime of ((int * int * int) * (int * int * int))
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("date", SDate (2024, 1, 15)),
    ("datetime", SDatetime ((2024, 1, 15), (12, 30, 0)))
]
val _ = my_data
