datatype val_t =
    SStr of string
  | SMap of (string * val_t) list
val shared_time : val_t = SStr "12:30:15+02:00"
val my_data : val_t = SMap [
    ("x", shared_time)
]
val _ = my_data
