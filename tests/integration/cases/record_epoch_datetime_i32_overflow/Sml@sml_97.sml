datatype val_t =
    SStr of string
  | SDatetime of ((int * int * int) * (int * int * int))
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("within_i32", SDatetime ((2024, 1, 15), (12, 0, 0))),
    ("beyond_i32", SDatetime ((2099, 6, 15), (8, 30, 0)))
]
val _ = my_data
